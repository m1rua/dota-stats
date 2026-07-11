import httpx

BASE_URL = "https://api.opendota.com/api"

def get_player_matches(account_id: int):
    response = httpx.get(f"{BASE_URL}/players/{account_id}/matches?limit=100", verify=False)
    return response.json()

def get_player_info(account_id: int):
    response = httpx.get(f"{BASE_URL}/players/{account_id}", verify=False)
    return response.json()

def get_player_wl(account_id: int, limit: int = 30):
    response = httpx.get(f"{BASE_URL}/players/{account_id}/wl?limit={limit}", verify=False)
    return response.json()

def get_heroes():
    response = httpx.get(f"{BASE_URL}/heroes", verify=False)
    return response.json()