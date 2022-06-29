
from typing import Union, List
from passlib.context import CryptContext
from fastapi import HTTPException, status
import schemas
import models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# users config passward
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()

def get_user_by_username(username: str):
    return models.User.filter(models.User.username == username).first()
def authenticate_user(username: str, password: str):
    # checking first if the user is in the database
    user = get_user_by_username(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, full_name="", verified=True, hashed_password=hashed_password)
    db_user.save()
    return db_user


# //handling post

def get_post(post_id: int):
    return models.Post.filter(models.Post.id == post_id).first()

def get_posts(skip: int = 0, limit: int = 100):
    return list(models.Post.select().offset(skip).limit(limit))


def create_user_post(*, title: str, description: Union[str, None] = None, image: Union[List, None] = None, created_at: str, user_id: int):
    # this is where your save the image to a bucket and return back the url to use
    # for now it is the image name we are saving
    post_data = schemas.PostCreate(title=title, image=image[0].filename, description=description, created_at=created_at)
    db_post = models.Post(**post_data.dict(), owner_id=user_id)
    db_post.save()
    return db_post

def update_user_post(post_data: schemas.Post, payload: schemas.PostUpdate):
    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_data, key, value)
        
    post_data.save()
    return post_data

def delete_post(post_data: schemas.Post):
    db_post = models.Post.get_by_id(post_data.id)
    db_post.delete_instance()