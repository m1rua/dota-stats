import asyncpg
import os
from dotenv import load_dotenv
import json

load_dotenv()

async def get_connection():
    return await asyncpg.connect(os.getenv("DATABASE_URL"), ssl=False)

async def get_cache(account_id):
    conn = await get_connection()
    result = await conn.fetchrow(
        """SELECT data FROM cache 
        WHERE account_id = $1 
        AND cached_at > NOW() - INTERVAL '1 hour'
        AND data->'matches'->0->>'hero_icon' IS NOT NULL""",
        account_id
    )
    await conn.close()
    return result

async def set_cache(account_id, data):
    conn = await get_connection()
    await conn.execute(
        "INSERT INTO cache (account_id, data) VALUES ($1, $2) ON CONFLICT (account_id) DO UPDATE SET data = $2, cached_at = NOW()",
        account_id, json.dumps(data)
    )
    await conn.close()