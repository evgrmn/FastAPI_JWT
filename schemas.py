import datetime as _dt
import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True


class _PostBase(_pydantic.BaseModel):
    post_text: str


class PostCreate(_PostBase):
    pass


class Post(_PostBase):
    id: int
    owner_id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True


class PostDelete(_pydantic.BaseModel):
    id: int

    class Config:
        orm_mode = True


class PostUpdate(_PostBase):
    id: int

    class Config:
        orm_mode = True


class PostLikeUpdate(_pydantic.BaseModel):
    id: int
    like: int

    class Config:
        orm_mode = True


# In-memory post likes and dislikes
class In_memory:
    from collections import defaultdict

    posts = defaultdict(lambda: {"likes": 0, "dislikes": 0})

