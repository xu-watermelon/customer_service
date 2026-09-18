import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from atguigu.config.config import settings


async def main():
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        tables = (await conn.execute(text("SHOW TABLES"))).fetchall()
        print("=== 所有表 ===")
        for row in tables:
            name = row[0]
            count = (await conn.execute(text(f"SELECT COUNT(*) FROM {name}"))).scalar()
            print(f"{name}: {count} 行")
    await engine.dispose()


asyncio.run(main())
