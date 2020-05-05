from marshmallow import fields, Schema

from fwork.common.schemas.constants import DICT_SCHEMA_EXCLUDED_FIELDS
from fwork.common.schemas.factory import make_model_request_schema
from source.models.comment import Comment

CommentBaseSchema = make_model_request_schema(Comment, exclude=DICT_SCHEMA_EXCLUDED_FIELDS + ('id',))


class CommentRequestSchema(Schema):
    """Useful for post query on comments"""
    comment = fields.Str(required=True, description='Comment for lead')
