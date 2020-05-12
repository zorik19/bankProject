from functools import partial

from marshmallow import fields

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema
from fwork.common.schemas.schema import FilterSchema
from source.models.lead import Lead, LeadSource, LeadStatus, LeadType

_make_schema = partial(make_model_request_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id',))

LeadBaseSchema = make_model_request_schema(Lead, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id', 'lead_hash'))
LeadStatusBaseSchema = _make_schema(LeadStatus)
LeadSourceBaseSchema = _make_schema(LeadSource)
LeadTypeBaseSchema = _make_schema(LeadType)


class LeadRequestSchema(LeadBaseSchema):
    class Meta:
        exclude = ('source_id',)


class LeadFilterSchema(FilterSchema):
    today = fields.Boolean(required=False, description='finish_at today', default=False)
    incoming = fields.Boolean(required=False, description='Not assigned leads', default=False)
    external_id = fields.Int(required=False, description='Assigned to a definite user')
