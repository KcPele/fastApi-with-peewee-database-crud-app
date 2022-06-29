from typing import Any, List, Union
from datetime import datetime
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class PostBase(BaseModel):
    description: Union[str, None] = None
    image: Union[str, None] = None
    
class PostCreateBase(PostBase):
    title: str
    created_at: datetime
class PostCreate(PostCreateBase):
    pass
class PostUpdate(PostBase):
    title: Union[str, None] = None

class Post(PostCreateBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    full_name: Union[str, None] = None
    verified: Union[bool, None] = None
    posts: List[Post] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

