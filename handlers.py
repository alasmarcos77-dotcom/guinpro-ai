from telegram import Update
from telegram.ext import ContextTypes
from app.odds import collect_sports, extract_candidates
from app.formatting import format_picks
from app.database import save_picks, summary

def _get_all():
    all_events, errors = [], []
    for category in ("futbol", "nba", "nfl"):
        events, errs = collect_sports(category)
        all_events.extend(events)
        errors.extend(errs)
    return extract_candidates(all_events), errors

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Bienvenido a AI BETTING ANALYST (@GuinProBot)!\\n"
        "Analizo cuotas disponibles de fútbol, NBA y NFL. Usa /help para ver comandos."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/picks — mejores cuotas encontradas\\n/futbol — fútbol\\n/nba — NBA\\n"
        "/nfl — NFL\\n/parlays — combinaciones exploratorias\\n/live — estado de datos\\n"
        "/resultados — historial\\n/roi — métricas registradas\\n/analizar — buscar un equipo o partido"
    )

async def _category(update, category, label):
    events, errors = collect_sports(category)
    items = extract_candidates(events)[:10]
    if items:
        save_picks(items)
    text = format_picks(items, label)
    if errors:
        text += "\\n\\nAvisos:\\n" + "\\n".join(errors[:3])
    await update.message.reply_text(text[:4000])

async def football(update, context): await _category(update, "futbol", "FÚTBOL")
async def nba(update, context): await _category(update, "nba", "NBA")
async def nfl(update, context): await _category(update, "nfl", "NFL")

async def picks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items, errors = _get_all()
    items = items[:10]
    if items: save_picks(items)
    text = format_picks(items)
    if errors: text += "\\n\\nAvisos:\\n" + "\\n".join(errors[:3])
    await update.message.reply_text(text[:4000])

async def parlays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items, errors = _get_all()
    items = items[:5]
    if len(items) < 2:
        await update.message.reply_text("No hay suficientes cuotas disponibles para proponer un parlay responsable.")
        return
    # These are illustrative combinations only; cross-event independence is not assumed.
    lines = ["🎯 COMBINACIONES EXPLORATORIAS", "No son recomendaciones con probabilidad conjunta validada."]
    for size in (2, 3, 4, 5):
        combo = items[:size]
        if len(combo) == size:
            combined = 1.0
            for p in combo: combined *= p["odds"]
            lines.append(f"\\n{size} selecciones | cuota combinada aproximada: {combined:.2f}")
            for p in combo: lines.append(f"• {p['event']} — {p['selection']} ({p['odds']:.2f})")
    lines.append("\\n⚠️ Correlaciones, margen de la casa y probabilidad real no están modelados.")
    await update.message.reply_text("\\n".join(lines)[:4000])

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("El módulo live aún no está conectado a un proveedor de marcadores en directo.")

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, won, lost, pending = summary()
    await update.message.reply_text(
        f"📊 PICKS REGISTRADOS\\nTotal: {total}\\nGanados: {won}\\nPerdidos: {lost}\\nPendientes: {pending}\\n"
        "La liquidación automática de resultados aún no está habilitada."
    )

async def roi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total, won, lost, pending = summary()
    settled = won + lost
    rate = (won / settled * 100) if settled else 0
    await update.message.reply_text(
        f"📈 MÉTRICAS\\nPicks: {total}\\nResueltos: {settled}\\nAcierto: {rate:.1f}%\\n"
        "ROI: no calculable todavía; falta registrar cuotas de cierre, stakes y resultados verificados."
    )

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()
    if not query:
        await update.message.reply_text("Uso: /analizar Real Madrid o /analizar Lakers")
        return
    await update.message.reply_text(
        f"Solicitud recibida: {query}\\nLa búsqueda específica de equipos/partidos se habilitará al conectar el proveedor de datos."
    )
