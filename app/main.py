from opendota import get_player_info, get_player_matches, get_player_wl
from fastapi import FastAPI

app = FastAPI()

@app.get("/player/{account_id}")
async def player_stats(account_id: int):
    info = await get_player_info(account_id)
    matches = await get_player_matches(account_id)
    wl = await get_player_wl(account_id)

    return {
        "info": info,
        "matches": matches,
        "wl":wl
    }