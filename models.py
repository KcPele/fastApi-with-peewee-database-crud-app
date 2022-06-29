import peewee

from database import db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    username = peewee.CharField(unique=True, index=True)
    full_name= peewee.CharField()
    hashed_password = peewee.CharField()
    verified = peewee.BooleanField(default=True)

    class Meta:
        database = db


class Post(peewee.Model):
    title = peewee.CharField(index=True)
    image = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    created_at = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="posts")

    class Meta:
        database = db
