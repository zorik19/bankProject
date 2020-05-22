from functools import partial

from marshmallow import fields

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_response_schema
from marshmallow_jsonapi import Schema

from source.models.lead import Lead, LeadSource, LeadStatus, LeadType

_make_schema = partial(make_model_response_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS)

LeadResponseBaseSchema = make_model_response_schema(Lead, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('lead_hash',),
                                                    type_='lead')
LeadStatusResponseSchema = _make_schema(LeadStatus, type_='lead_statuses')
LeadSourceResponseSchema = _make_schema(LeadSource, type_='lead_source')
LeadTypeResponseSchema = _make_schema(LeadType, type_='lead_type')


class LeadResponseSchema(LeadResponseBaseSchema):
    status = fields.String(description='lead status interpreted to string ')
    source = fields.String(description='lead source interpreted to string ')
    type = fields.String(description='lead type interpreted to string ')


class LeadXLSXResponseSchema(Schema):
    id = fields.Int(description='Just for json-api compatibility')
    uploaded = fields.Int(description='How many rows were uploaded successfully')
    errors = fields.List(fields.Dict(description='Error message detail'), description='Errors list')
    error_count = fields.Int(description='How many rows were rejected (didn\'t uploaded)')

    class Meta:
        type_ = 'xlsx_upload'
