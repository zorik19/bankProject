from io import BytesIO

import sqlalchemy as sa
from fwork.common.auth import authorized
from fwork.common.auth.token import get_auth_payload_from_request
from fwork.common.db.postgres.conn_async import db
from fwork.common.http import HTTPStatus
from fwork.common.http.response import BadRequestResponse, CreatedResponse, SingleEntityResponse
from fwork.common.logs.sanic_helpers import TrackedRequest
from fwork.common.openapi.spec import DocMixin, error_responses, many_response, request_body, \
    single_response
from fwork.common.sanic.crud.factory import make_view
from fwork.common.sanic.crud.requests import raw_args
from fwork.common.sanic.crud.views import PagedEntitiesView, SingleEntityView
from fwork.common.schemas.request_args import IntPaginationSchema, RawPaginationSchema
from sanic import response
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from source.application.utils.hash import hash_payload
from source.application.utils.xlsx import generate_xlsx, parse_xlsx
from source.constants import FORMAT_TO_MIME_TYPE, LeadSourceType, LeadStatusEnum
from source.logger import get_logger
from source.models.lead import Lead, LeadSource, LeadStatus, LeadType
from source.schemas.lead import LeadBaseSchema, LeadFilterSchema, LeadRequestSchema, LeadSourceBaseSchema, \
    LeadStatusBaseSchema, LeadTypeBaseSchema
from source.schemas.response_schemas.lead import LeadResponseBaseSchema, LeadResponseSchema, \
    LeadSourceResponseSchema, \
    LeadStatusResponseSchema, LeadTypeResponseSchema, LeadXLSXResponseSchema

log = get_logger('lead')

decorators = [authorized]

LeadBaseView = make_view(SingleEntityView,
                         Lead,
                         LeadResponseBaseSchema,
                         log,
                         decorators,
                         enable_delete=True)
LeadsBaseView = make_view(PagedEntitiesView, Lead, LeadResponseSchema, log, decorators)

lead_source_views_common = (LeadSource, LeadSourceResponseSchema, log, decorators)
LeadSourcesBaseView = make_view(PagedEntitiesView, *lead_source_views_common)

lead_status_views_common = (LeadStatus, LeadStatusResponseSchema, log, decorators)
LeadStatusesBaseView = make_view(PagedEntitiesView, *lead_status_views_common)

lead_type_views_common = (LeadType, LeadTypeResponseSchema, log, decorators)
LeadTypesBaseView = make_view(PagedEntitiesView, *lead_type_views_common)


class LeadsView(DocMixin, LeadsBaseView):
    PAGING_SCHEMA = RawPaginationSchema
    FILTER_SCHEMA = LeadFilterSchema

    def base_get_query(self, request, url_params):

        query = db.select([*Lead.t.c,
                           LeadStatus.t.c.description.label('status'),
                           LeadSource.t.c.description.label('source'),
                           LeadType.t.c.description.label('type')]) \
            .select_from(Lead.t
                         .outerjoin(LeadStatus.t) \
                         .outerjoin(LeadSource.t) \
                         .outerjoin(LeadType.t)) \
            .order_by(self.MODEL_CLASS.finish_at.desc()) \
            .order_by(self.MODEL_CLASS.created_at.desc()) \
            .order_by(self.MODEL_CLASS.id)

        if url_params.get('incoming'):
            query = query.where(Lead.external_id == None) \
                .where(sa.or_(Lead.status_id.notin_([LeadStatusEnum.DENIAL.value, LeadStatusEnum.PRODUCTION.value]),
                              Lead.status_id == None))

        if url_params.get('external_id'):
            query = query.where(Lead.external_id == url_params['external_id']) \
                .where(sa.or_(Lead.status_id.notin_([LeadStatusEnum.DENIAL.value, LeadStatusEnum.PRODUCTION.value]),
                              Lead.status_id == None)) \
                .order_by(self.MODEL_CLASS.in_progress)

        if url_params.get('status_id'):
            query = query.where(Lead.status_id == url_params['status_id'])

        if url_params.get('date_from'):
            query = query.where(sa.func.date(Lead.finish_at) >= url_params['date_from'])

        if url_params.get('date_to'):
            query = query.where(sa.func.date(Lead.finish_at) <= url_params['date_to'])

        # FOR DEBUG
        # build = query.compile(dialect=sa.dialects.postgresql.dialect())
        # log.debug(f'QUERY: {build}')
        # log.debug(f'PARAMS: {build.params}')

        return query

    def get_collection_query(self, request, url_params, log):
        """
        override this method to avoid filtering, as we have custom filters
        """
        query = self.base_get_query(request, url_params)
        parser = self.REQUEST_PARSER(self, request, url_params)

        helper = self.QUERY_HELPER(self.MODEL_CLASS, query=query, log=log)
        helper.add_order(parser.get_order())
        helper.add_paging(parser.get_paging())

        return helper.query

    @doc.summary('Get list of leads')
    @doc.description('Get list of available leads')
    @doc.response(200, many_response(LeadResponseSchema), description='List of leads')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        raw_params = raw_args(request)
        query_params = self.FILTER_SCHEMA().load(raw_params)
        return await super().get(request, **query_params)

    @doc.summary('Create new Lead')
    @doc.description('Create new Lead with manual source type')
    @doc.consumes(request_body(LeadRequestSchema), location='body')
    @doc.response(201, 'lead created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadBaseSchema().load(request.json)
        data['source_id'] = LeadSourceType.MANUAL.value
        lead_hash = hash_payload(data)
        data['lead_hash'] = lead_hash
        lead = await Lead.create(**data)
        log.debug(f'lead created {lead}')
        return CreatedResponse('Lead successfully created')


class LeadView(DocMixin, LeadBaseView):
    @doc.summary('Get lead by id')
    @doc.description('Get lead by id')
    @doc.response(200, single_response(LeadResponseBaseSchema), description='lead')
    @error_responses(401)
    async def get(self, request: TrackedRequest, **url_params) -> HTTPResponse:
        return await super().get(request, **url_params)

    @doc.summary('Update lead by id')
    @doc.description('Update lead by id wih new status')
    @doc.consumes(request_body(LeadBaseSchema), location='body')
    @doc.response(200, single_response(LeadResponseBaseSchema), description='Updated lead')
    @error_responses(401)
    async def patch(self, request: TrackedRequest, lead_id: int) -> HTTPResponse:
        token_payload = get_auth_payload_from_request(request)
        user_id = token_payload['sub']

        updates = LeadBaseSchema().load(request.json)
        status_id = updates.get('status_id')
        in_progress = updates.get('in_progress')

        if in_progress:
            lead_in_progress = await Lead.query.where(Lead.external_id == user_id) \
                .where(Lead.in_progress == True) \
                .gino.first()

            if lead_in_progress:
                return BadRequestResponse(f'You already have Lead IN PROGRESS lead_id:{lead_in_progress.id}')

        async with db.transaction() as tx:
            lead_q = Lead.query.where(Lead.id == lead_id).with_for_update()
            lead = await lead_q.gino.first()

            if status_id and ((status_id == LeadStatusEnum.CHANGE_TIME.value) or (
                    status_id != lead.status_id and lead.in_progress)):
                # on change status we need to stop progress for this lead
                updates['in_progress'] = False

            await lead.update(**updates).apply()
            updated = await Lead.get(lead_id)

        return SingleEntityResponse(updated, LeadResponseBaseSchema)

    @doc.summary('delete lead by id')
    @doc.description('Update lead by id wih new status')
    @doc.response(HTTPStatus.NO_CONTENT, 'Successfully deleted', 'No content response')
    @error_responses(401)
    async def delete(self, request: TrackedRequest, lead_id: int) -> HTTPResponse:
        return await super().delete(request, lead_id)


class LeadFileView(DocMixin, HTTPMethodView):
    @doc.summary('Download template file')
    @doc.description('Download template file of leads in different formats like `csv`, `xlsx`')
    @doc.consumes(doc.String(name='format', required=True, description='Format of input data'),
                  location='query')
    @doc.response(200, 'OK', description='Leads uploaded successfully')
    async def get(self, request) -> HTTPResponse:
        data = generate_xlsx()

        headers = {'Content-Disposition': f'attachment; filename="{data.name}"', }

        return response.raw(data.getvalue(),
                            headers=headers,
                            content_type=FORMAT_TO_MIME_TYPE['xlsx'],
                            )

    @doc.summary('Upload file of leads')
    @doc.description('Upload file of leads in different formats like `csv`, `xlsx`')
    @doc.consumes(doc.String(name='format', required=True, description='Format of input data'),
                  location='query')
    @doc.consumes(
        doc.File(name="file"), location="formData", content_type="multipart/form-data"
        )
    @doc.response(200, single_response(LeadXLSXResponseSchema), description='Leads uploaded statistic')
    async def post(self, request) -> HTTPResponse:
        if not request.body:
            log.debug('Request body is empty')
            return BadRequestResponse('Request body is empty')

        xlsx_file = BytesIO(request.body)
        uploaded, error_count, errors = await parse_xlsx(xlsx_file)
        data = {'uploaded': uploaded,
                'errors': errors,
                'error_count': error_count}
        return SingleEntityResponse(data, LeadXLSXResponseSchema)


class LeadStatusesView(DocMixin, LeadStatusesBaseView):
    PAGING_SCHEMA = IntPaginationSchema

    @doc.summary('Get list of lead statues')
    @doc.description('Get list of available lead statuses')
    @doc.response(200, many_response(LeadStatusResponseSchema), description='List of lead statuses')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead status')
    @doc.description('Create new Lead status')
    @doc.consumes(request_body(LeadStatusBaseSchema), location='body')
    @doc.response(201, 'lead status created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadStatusBaseSchema().load(request.json)
        lead = await LeadStatus.create(**data)
        log.debug(f'lead created {lead}')

        return CreatedResponse('Lead status successfully created')


class LeadSourcesView(DocMixin, LeadSourcesBaseView):
    PAGING_SCHEMA = IntPaginationSchema

    @doc.summary('Get list of lead sources')
    @doc.description('Get list of available lead sources')
    @doc.response(200, many_response(LeadSourceResponseSchema), description='List of lead sources')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead source')
    @doc.description('Create new Lead source')
    @doc.consumes(request_body(LeadSourceBaseSchema), location='body')
    @doc.response(201, 'lead created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadSourceBaseSchema().load(request.json)
        lead = await LeadSource.create(**data)
        log.debug(f'lead created {lead}')

        return CreatedResponse('Lead source successfully created')


class LeadTypesView(DocMixin, LeadTypesBaseView):
    PAGING_SCHEMA = IntPaginationSchema

    @doc.summary('Get list of lead types')
    @doc.description('Get list of available lead types')
    @doc.response(200, many_response(LeadTypeResponseSchema), description='List of lead types')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead type')
    @doc.description('Create new Lead type')
    @doc.consumes(request_body(LeadTypeBaseSchema), location='body')
    @doc.response(201, 'lead  type created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadTypeBaseSchema().load(request.json)
        lead = await LeadType.create(**data)
        log.debug(f'lead created {lead}')

        return CreatedResponse('Lead source successfully created')
