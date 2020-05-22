from datetime import datetime, time
from functools import partial

import pytz
from marshmallow import fields, post_load, pre_load, Schema

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema
from fwork.common.schemas.schema import FilterSchema
from source.constants import LEAD_TYPE_TO_ID
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


class LeadXLSXSchema(Schema):
    auction = fields.Str(required=False, allow_none=True, description='№ Аукциона')
    incoming_date = fields.DateTime(required=False, allow_none=True, description='Дата')
    amount = fields.Float(required=False, allow_none=True, description='Сумма БГ', )
    name = fields.Str(required=False, allow_none=True, description='Название')
    inn = fields.Str(required=False, allow_none=True, description='ИНН')
    email = fields.Str(required=False, allow_none=True, description='E-mail')
    lead_person = fields.Str(required=False, allow_none=True, description='Конт. Лицо')
    description = fields.Str(required=False, allow_none=True, description='Описание')
    phone_number = fields.Str(required=False, allow_none=True, description='Телефон')
    federal_law = fields.Str(required=False, allow_none=True, description='ФЗ')
    region = fields.Str(required=False, allow_none=True, description='Регион')
    type_id = fields.Int(required=False, allow_none=True, description='Наименование базы')

    @pre_load(pass_many=False)
    def load_db_type(self, data, many, **kwargs):
        type_id = 'type_id'
        if data.get(type_id):
            data[type_id] = LEAD_TYPE_TO_ID.get(data[type_id].lower())
        return data

    def reverse_field_mapping(self):
        ...


# TODO: maybe useless, if it so - rm
class LeadSchema(LeadXLSXSchema):
    external_id = fields.Int(required=False, description='ID пользователя из сервиса авторизации')
    status_id = fields.Int(required=False, description='Статус')
    source_id = fields.Int(required=False, description='Источник создания')
    in_progress = fields.Bool(allow_none=False, description="Флаг взятия в работу")
    feedback_type = fields.Str(required=False,
                               description='email')  # TODO: enum or ForeignKey in future  or even delete
    contacts = fields.Dict(description='Дополнительные контакты пользователя')
    lead_hash = fields.Str(required=False, description='md5 чек сумма полей')
    finish_at = fields.Date(required=False, description='Время завершения')
