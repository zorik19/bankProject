from sanic_openapi import swagger_blueprint

from fwork.common.env.version import get_app_version
from fwork.common.sanic.app import make_app, run_app
from source.application.endpoints.comment import CommentsView, CommentView
from source.application.endpoints.lead import LeadFileView, LeadSourcesView, LeadStatusesView, LeadsView, LeadTypesView, \
    LeadView
from source.constants import PROJECT_NAME

app = make_app(PROJECT_NAME, use_postgres=True, use_sentry=False)

app.config.API_DESCRIPTION = f"{app.name} service API, app version: {get_app_version()}"

V1 = '/api/v1'
# Register views to handle requests.
app.add_route(LeadsView.as_view(), f'{V1}/leads')
app.add_route(LeadFileView.as_view(), f'{V1}/leads/file')
app.add_route(LeadStatusesView.as_view(), f'{V1}/lead_statuses')
app.add_route(LeadView.as_view(), f'{V1}/leads/<lead_id:int>')
app.add_route(LeadSourcesView.as_view(), f'{V1}/lead_sources/')
app.add_route(LeadTypesView.as_view(), f'{V1}/lead_types/')
app.add_route(CommentsView.as_view(), f'{V1}/leads/<lead_id:int>/comments')
app.add_route(CommentView.as_view(), f'{V1}/comments/<comment_id:int>')

# Enable OpenApi spec generation
app.blueprint(swagger_blueprint)

# Should help to use templates only once per instance

if __name__ == "__main__":
    run_app(app)
