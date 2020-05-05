from fwork.common.schemas.factory import make_model_response_schema
from source.models.comment import Comment

# for comments return times
CommentResponseSchema = make_model_response_schema(Comment, type_='comment', )
