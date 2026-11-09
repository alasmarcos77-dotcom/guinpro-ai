import logging
from telegram.ext import Application, CommandHandler
from app.config import settings
from app.handlers import (
    start, help_command, picks, football, nba, nfl, parlays,
    live, results, roi, analyze
)
from app.scheduler import configure_jobs

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def main():
    if not settings.telegram_bot_token:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en las variables de entorno.")
    app = Application.builder().token(settings.telegram_bot_token).build()
    handlers = [
        ("start", start), ("help", help_command), ("picks", picks),
        ("futbol", football), ("nba", nba), ("nfl", nfl),
        ("parlays", parlays), ("live", live), ("resultados", results),
        ("roi", roi), ("analizar", analyze),
    ]
    for command, callback in handlers:
        app.add_handler(CommandHandler(command, callback))
    configure_jobs(app)
    logger.info("AI BETTING ANALYST iniciado.")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
