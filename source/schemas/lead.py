from datetime import datetime, time
from functools import partial

import pytz
from marshmallow import fields, post_load

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema
from fwork.common.schemas.schema import FilterSchema
from source.models.lead import Lead, LeadSource, LeadStatus, LeadType

_make_schema = partial(make_model_request_schema, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id',))

LeadBaseSchema = make_model_request_schema(Lead, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id', 'lead_hash'),
                                           allow_none=True)
LeadStatusBaseSchema = _make_schema(LeadStatus)
LeadSourceBaseSchema = _make_schema(LeadSource)
LeadTypeBaseSchema = _make_schema(LeadType)


class LeadRequestSchema(LeadBaseSchema):
    class Meta:
        exclude = ('source_id',)


class LeadFilterSchema(FilterSchema):
    incoming = fields.Boolean(required=False, description='Not assigned leads', default=False)
    external_id = fields.Int(required=False, description='Assigned to a definite user')
    date_from = fields.Date(required=False, description='finish_at from date %Y-%m-%d')
    date_to = fields.Date(required=False, description='finish_at to date %Y-%m-%d')
    status_id = fields.Int(required=False, description='Lead status filter')

    @post_load
    def convert_timezone(self, data, **kwargs):

        for key in ('date_from', 'date_to'):
            if key not in data:
                continue
            data[key] = pytz.utc.localize(datetime.combine(data[key], time.min))

        return data
