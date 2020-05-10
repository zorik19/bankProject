from marshmallow import fields

from fwork.common.schemas.factory import make_model_response_schema
from source.models.comment import Comment

# for comments return times
CommentResponseBaseSchema = make_model_response_schema(Comment, type_='comment', )


class CommentResponseSchema(CommentResponseBaseSchema):
    status = fields.String(description='lead status interpreted to string ')
