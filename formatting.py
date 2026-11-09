from datetime import datetime
from zoneinfo import ZoneInfo
from app.config import settings

def format_picks(items, title="MEJORES CUOTAS DISPONIBLES"):
    if not items:
        return "No hay selecciones disponibles con los filtros actuales. No se inventarán picks."
    lines = [f"🏟️ AI BETTING ANALYST — {title}", ""]
    for i, p in enumerate(items, 1):
        try:
            local_dt = datetime.fromisoformat(p["commence"].replace("Z", "+00:00")).astimezone(ZoneInfo(settings.timezone))
            date = local_dt.strftime("%d/%m %H:%M")
        except Exception:
            date = "Horario por confirmar"
        lines.append(
            f"{i}. {p['sport']} | {p['event']}\n"
            f"   Selección: {p['selection']} | Cuota: {p['odds']:.2f}\n"
            f"   Prob. implícita de cuota: {p['implied']*100:.1f}% | {p['bookmaker']}\n"
            f"   Inicio: {date}"
        )
    lines += ["", "⚠️ Son cuotas y probabilidades implícitas del mercado, no predicciones propias ni garantías. Verifica lesiones, alineaciones y cuotas antes de apostar."]
    return "\n".join(lines)
