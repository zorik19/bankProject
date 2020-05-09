from functools import partial

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_response_schema
from source.models.lead import Lead, LeadSource, LeadStatus

_make_schema = partial(make_model_response_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS)

LeadResponseSchema = make_model_response_schema(Lead, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('lead_hash',), type_='lead')
LeadStatusResponseSchema = _make_schema(LeadStatus, type_='lead_statuses')
LeadSourceResponseSchema = _make_schema(LeadSource, type_='lead_source')
