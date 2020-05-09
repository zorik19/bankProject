from functools import partial

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema
from source.models.lead import Lead, LeadSource, LeadStatus

_make_schema = partial(make_model_request_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id',))

LeadBaseSchema = make_model_request_schema(Lead, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id', 'lead_hash'))
LeadStatusBaseSchema = _make_schema(LeadStatus)
LeadSourceBaseSchema = _make_schema(LeadSource)


class LeadRequestSchema(LeadBaseSchema):
    class Meta:
        exclude = ('source_id',)
