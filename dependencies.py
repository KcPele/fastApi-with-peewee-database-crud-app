
from fastapi import Depends
import database
import models
from database import db_state_default

database.db.connect()
database.db.create_tables([models.User, models.Post])
database.db.close()


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()
