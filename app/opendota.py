import httpx

BASE_URL = "https://api.opendota.com/api"

async def get_player_matches(account_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/players/{account_id}/matches?limit=30")
        return response.json()

async def get_player_info(account_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/players/{account_id}")
        return response.json()

async def get_player_wl(account_id: int, limit: int = 30):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/players/{account_id}/wl?limit={limit}")
        return response.json()
