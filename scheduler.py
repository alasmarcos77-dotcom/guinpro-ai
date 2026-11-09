from datetime import time
from zoneinfo import ZoneInfo
from telegram.ext import ContextTypes
from app.config import settings
from app.handlers import _get_all
from app.formatting import format_picks

async def _send_daily(context: ContextTypes.DEFAULT_TYPE):
    # Telegram bots cannot broadcast to users until they have started the bot.
    # Set TELEGRAM_CHAT_ID to the chat that should receive scheduled reports.
    import os
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not chat_id:
        return
    items, errors = _get_all()
    text = format_picks(items[:10])
    if errors: text += "\\n\\nAvisos:\\n" + "\\n".join(errors[:2])
    await context.bot.send_message(chat_id=chat_id, text=text[:4000])

def configure_jobs(app):
    if app.job_queue is None:
        return
    tz = ZoneInfo(settings.timezone)
    app.job_queue.run_daily(_send_daily, time=time(settings.daily_picks_hour, 0, tzinfo=tz), name="morning-picks")
    app.job_queue.run_daily(_send_daily, time=time(settings.update_hour, 0, tzinfo=tz), name="afternoon-update")
