import requests
from app.config import settings

BASE = "https://api.the-odds-api.com/v4"

SPORTS = {
    "futbol": [
        "soccer_epl", "soccer_spain_la_liga", "soccer_germany_bundesliga",
        "soccer_italy_serie_a", "soccer_france_ligue_one",
        "soccer UEFA champions league".replace(" ", "_"),
    ],
    "nba": ["basketball_nba"],
    "nfl": ["americanfootball_nfl"],
}

def fetch_odds(sport_key):
    if not settings.odds_api_key:
        return [], "Falta configurar ODDS_API_KEY."
    url = f"{BASE}/sports/{sport_key}/odds"
    params = {
        "apiKey": settings.odds_api_key,
        "regions": settings.default_regions,
        "markets": "h2h",
        "oddsFormat": "decimal",
        "dateFormat": "iso",
    }
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return [], f"No se pudieron consultar las cuotas: {exc}"

def collect_sports(category):
    events, errors = [], []
    for key in SPORTS.get(category, []):
        data, error = fetch_odds(key)
        if error:
            errors.append(f"{key}: {error}")
        else:
            events.extend(data)
    return events, errors

def extract_candidates(events):
    candidates = []
    for event in events:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market.get("key") != "h2h":
                    continue
                for outcome in market.get("outcomes", []):
                    price = outcome.get("price")
                    if isinstance(price, (int, float)) and 1.50 <= price <= 2.20:
                        candidates.append({
                            "sport": event.get("sport_title", "Deporte"),
                            "event": f'{event.get("home_team")} vs {event.get("away_team")}',
                            "selection": outcome.get("name"),
                            "odds": float(price),
                            "bookmaker": bookmaker.get("title", "Casa no indicada"),
                            "commence": event.get("commence_time", ""),
                            "implied": 1 / float(price),
                        })
    # Prefer best prices per event/selection; do not imply model confidence.
    unique = {}
    for item in candidates:
        key = (item["event"], item["selection"])
        if key not in unique or item["odds"] > unique[key]["odds"]:
            unique[key] = item
    return sorted(unique.values(), key=lambda x: x["odds"], reverse=True)
