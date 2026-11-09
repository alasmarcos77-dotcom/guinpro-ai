import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    odds_api_key: str = os.getenv("ODDS_API_KEY", "")
    timezone: str = os.getenv("TZ", "America/El_Salvador")
    daily_picks_hour: int = int(os.getenv("DAILY_PICKS_HOUR", "7"))
    update_hour: int = int(os.getenv("UPDATE_HOUR", "15"))
    default_regions: str = os.getenv("ODDS_REGIONS", "us")
    max_picks: int = int(os.getenv("MAX_PICKS", "10"))

settings = Settings()
