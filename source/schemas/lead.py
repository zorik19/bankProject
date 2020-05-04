from functools import partial

from source.models.lead import Lead, LeadSource, LeadStatus
from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema

_make_schema = partial(make_model_request_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id',))

LeadBaseSchema = _make_schema(Lead)
LeadStatusBaseSchema = _make_schema(LeadStatus)
LeadSourceBaseSchema = _make_schema(LeadSource)
