from opendota import get_player_info, get_player_matches, get_player_wl, get_heroes
from fastapi import FastAPI
from db import set_cache, get_cache
app = FastAPI()

@app.get("/player/{account_id}")
async def player_stats(account_id: int):
    cached = await get_cache(account_id)
    if cached:
        return cached["data"]
    info = get_player_info(account_id)
    matches = get_player_matches(account_id)
    wl = get_player_wl(account_id)
    all_heroes = get_heroes()


    total_kills = sum(m["kills"] for m in matches)
    total_death = sum(m["deaths"] for m in matches)
    total_assists = sum(m["assists"] for m in matches)
    winrate = wl["win"] / (wl["win"] + wl["lose"]) * 100
    heroes_map = {h["id"]: h["localized_name"] for h in all_heroes}
    avg_kda = round((total_kills + total_assists) / total_death, 2)


    heroes = {}
    for m in matches:
        hero = m["hero_id"]
        if hero not in heroes:
            heroes[hero] = {"games": 0, "wins": 0}
        heroes[hero]["games"] += 1
        is_radiant = m["player_slot"] < 128
        won = (is_radiant and m["radiant_win"]) or (not is_radiant and not m["radiant_win"])
        if won:
            heroes[hero]["wins"] += 1

    top3 = sorted(heroes.items(), key=lambda x: x[1]["games"], reverse=True)[:3]
    top3_named = [
        {"hero": heroes_map.get(hero_id, hero_id), "games": stats["games"], "wins": stats["wins"]}
         for hero_id, stats in top3
    ]

    result = {
        "info": info,
        "matches": matches,
        "wl": wl,
        "winrate": winrate,
        "avg_kda": avg_kda,
        "top3": top3_named
    }
    await set_cache(account_id, result)
    return result