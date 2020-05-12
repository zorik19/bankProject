from sanic.response import HTTPResponse
from sanic_openapi import doc

from fwork.common.auth import authorized
from fwork.common.auth.token import get_auth_payload_from_request
from fwork.common.db.postgres.conn_async import db
from fwork.common.http import HTTPStatus
from fwork.common.http.response import CreatedResponse
from fwork.common.logs.sanic_helpers import TrackedRequest
from fwork.common.openapi.spec import DocMixin, error_responses, many_response, request_body, single_response
from fwork.common.sanic.crud.factory import make_view
from fwork.common.sanic.crud.views import PagedEntitiesView, SingleEntityView
from fwork.common.schemas.request_args import RawPaginationSchema
from source.logger import get_logger
from source.models.comment import Comment
from source.models.lead import Lead, LeadStatus
from source.schemas.comment import CommentBaseSchema, CommentRequestSchema
from source.schemas.response_schemas.comment import CommentResponseSchema

log = get_logger('comment')

decorators = [authorized]

comment_views_common = (Comment, CommentResponseSchema, log, decorators)
CommentBaseView = make_view(SingleEntityView, *comment_views_common,
                            enable_delete=True,
                            enable_patch=True,
                            patch_request_schema=CommentBaseSchema,
                            patch_response_schema=CommentResponseSchema)
CommentsBaseView = make_view(PagedEntitiesView, *comment_views_common)


class CommentsView(DocMixin, CommentsBaseView):
    PAGING_SCHEMA = RawPaginationSchema

    def base_get_query(self, request, url_params: dict):
        """
        Of course we know tthat we can send lead_id directly - but then we cant use `dynamic` query generation
        :param request:
        :param url_params: dict from request like {"lead_id":231}
        :return: SQLAlchemy.Query
        """
        lead_id = url_params['lead_id']
        query = db.select([*Comment.t.c, LeadStatus.t.c.description.label('status')]) \
            .select_from(Comment.t
                         .join(LeadStatus.t)) \
            .where(Comment.lead_id == lead_id) \
            .order_by(Comment.t.c.created_at.desc())

        return query

    @doc.summary('Get list of comments')
    @doc.description('Get list of available comments')
    @doc.response(200, many_response(CommentResponseSchema), description='List of comments')
    @error_responses(401)
    async def get(self, request: TrackedRequest, **url_params) -> HTTPResponse:
        return await super().get(request, **url_params)

    @doc.summary('Create new Comment')
    @doc.description('Create new Comment')
    @doc.consumes(request_body(CommentRequestSchema), location='body')
    @doc.response(201, 'comment created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest, lead_id: int) -> HTTPResponse:
        data = CommentRequestSchema().load(request.json)

        token_payload = get_auth_payload_from_request(request)
        user_id = token_payload['sub']

        # doesn't matter which external_id was
        data['external_id'] = user_id
        data['lead_id'] = lead_id

        async with db.transaction() as tx:
            lead_q = Lead.query.where(Lead.id == lead_id).with_for_update()
            lead = await lead_q.gino.first()
            comment = await Comment.create(**data)
            await lead.update(status_id=data['status_id']).apply()

        log.debug(f'comment created {comment}')

        return CreatedResponse('Comment successfully created')


class CommentView(DocMixin, CommentBaseView):

    @doc.summary('Get comment by id')
    @doc.description('Get comment by definite id')
    @doc.response(200, single_response(CommentResponseSchema), description='comment')
    @error_responses(401)
    async def get(self, request: TrackedRequest, **url_params) -> HTTPResponse:
        return await super().get(request, **url_params)

    @doc.summary('Update comment by id')
    @doc.description('Update comment by id wih new status')
    @doc.consumes(request_body(CommentBaseSchema), location='body')
    @doc.response(200, single_response(CommentResponseSchema), description='Updated comment')
    @error_responses(401)
    async def patch(self, request: TrackedRequest, comment_id: int) -> HTTPResponse:
        return await super().patch(request, comment_id)

    @doc.summary('delete comment by id')
    @doc.description('Delete comment by id')
    @doc.response(HTTPStatus.NO_CONTENT, 'Successfully deleted', 'No content response')
    @error_responses(401)
    async def delete(self, request: TrackedRequest, comment_id: int) -> HTTPResponse:
        return await super().delete(request, comment_id)
