from sanic.response import HTTPResponse
from sanic_openapi import doc

from fwork.common.auth import authorized
from fwork.common.http import HTTPStatus
from fwork.common.http.response import CreatedResponse
from fwork.common.logs.sanic_helpers import TrackedRequest
from fwork.common.openapi.spec import DocMixin, error_responses, many_response, request_body, single_response
from fwork.common.sanic.crud.factory import make_view
from fwork.common.sanic.crud.views import PagedEntitiesView, SingleEntityView
from fwork.common.schemas.request_args import IntPaginationSchema
from source.logger import get_logger
from source.models.lead import Lead, LeadSource, LeadStatus
from source.schemas.lead import LeadBaseSchema, LeadSourceBaseSchema, LeadStatusBaseSchema
from source.schemas.response_schemas.lead import LeadResponseSchema, LeadSourceResponseSchema, LeadStatusResponseSchema

log = get_logger('lead')

decorators = [authorized]

lead_views_common = (Lead, LeadResponseSchema, log, decorators)
LeadBaseView = make_view(SingleEntityView, *lead_views_common, enable_delete=True, enable_patch=True,
                         patch_request_schema=LeadBaseSchema, patch_response_schema=LeadResponseSchema)
LeadsBaseView = make_view(PagedEntitiesView, *lead_views_common)

lead_source_views_common = (LeadSource, LeadSourceResponseSchema, log, decorators)
LeadSourcesBaseView = make_view(PagedEntitiesView, *lead_source_views_common)

lead_status_views_common = (LeadStatus, LeadStatusResponseSchema, log, decorators)
LeadStatusesBaseView = make_view(PagedEntitiesView, *lead_status_views_common)


class LeadsView(DocMixin, LeadsBaseView):
    PAGING_SCHEMA = IntPaginationSchema

    @doc.summary('Get list of leads')
    @doc.description('Get list of available leads')
    @doc.response(200, many_response(LeadResponseSchema), description='List of leads')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead')
    @doc.description('Create new Lead')
    @doc.consumes(request_body(LeadBaseSchema), location='body')
    @doc.response(201, 'lead created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadBaseSchema().load(request.json)
        lead = await Lead.create(**data)
        log.debug(f'lead created {lead}')

        return CreatedResponse('Lead successfully created')


class LeadView(DocMixin, LeadBaseView):
    @doc.summary('Get lead by id')
    @doc.description('Get lead by id')
    @doc.response(200, single_response(LeadResponseSchema), description='lead')
    @error_responses(401)
    async def get(self, request: TrackedRequest, **url_params) -> HTTPResponse:
        return await super().get(request, **url_params)

    @doc.summary('Update lead by id')
    @doc.description('Update lead by id wih new status')
    @doc.consumes(request_body(LeadBaseSchema), location='body')
    @doc.response(200, single_response(LeadResponseSchema), description='Updated lead')
    @error_responses(401)
    async def patch(self, request: TrackedRequest, lead_id: int) -> HTTPResponse:
        return await super().patch(request, lead_id)

    @doc.summary('delete lead by id')
    @doc.description('Update lead by id wih new status')
    @doc.response(HTTPStatus.NO_CONTENT, 'Successfully deleted', 'No content response')
    @error_responses(401)
    async def delete(self, request: TrackedRequest, lead_id: int) -> HTTPResponse:
        return await super().delete(request, lead_id)


class LeadStatusesView(DocMixin, LeadStatusesBaseView):
    PAGING_SCHEMA = IntPaginationSchema

    @doc.summary('Get list of lead statues')
    @doc.description('Get list of available lead statuses')
    @doc.response(200, many_response(LeadResponseSchema), description='List of lead statuses')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead status')
    @doc.description('Create new Lead')
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
    @doc.response(200, many_response(LeadResponseSchema), description='List of lead sources')
    @error_responses(401)
    async def get(self, request: TrackedRequest) -> HTTPResponse:
        return await super().get(request)

    @doc.summary('Create new Lead')
    @doc.description('Create new Lead')
    @doc.consumes(request_body(LeadSourceBaseSchema), location='body')
    @doc.response(201, 'lead created', description='Created response')
    @error_responses(401)
    async def post(self, request: TrackedRequest) -> HTTPResponse:
        data = LeadSourceBaseSchema().load(request.json)
        lead = await LeadSource.create(**data)
        log.debug(f'lead created {lead}')

        return CreatedResponse('Lead source successfully created')
