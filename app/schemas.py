from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# We don't need PostList anymore, we'll use List[PostResponse] directly in our route