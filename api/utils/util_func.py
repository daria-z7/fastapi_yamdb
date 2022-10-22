from sqlalchemy.future import select
from sqlalchemy import func

from db.db_setup import database

async def check_if_exists(model, id: int):
    query = select(func.count(model.id)).where(model.id==id)
    record_count = await database.fetch_val(query)
    if record_count > 0:
        return True
    return False
