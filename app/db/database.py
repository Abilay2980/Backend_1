import asyncpg
from app.core.config import settings


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=settings.DB_USER,
            password=settings.DB_PASS,
            database=settings.DB_NAME,
            host=settings.DB_HOST,
            port=int(settings.DB_PORT),
        )
        print("Database is connected")

    async def disconnect(self):
        await self.pool.close()
        print("Database is disconnected")

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            rows=  await conn.fetch(query, *args)
            result = [dict(row) for row in rows]
            return result

    async def get_db_connection(self):
        async with self.pool.acquire() as conn:
            yield conn

db = Database()
