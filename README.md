# AI BETTING ANALYST — GuinProBot

Bot de Telegram para consultar cuotas de fútbol, NBA y NFL, con reportes programados.

## Importante: alcance de esta primera versión
- Consulta cuotas de The Odds API; requiere `ODDS_API_KEY`.
- Muestra cuotas decimales entre 1.50 y 2.20 y su probabilidad implícita (`1/cuota`).
- **No calcula todavía probabilidades propias ni ventaja estadística (EV)**. Una cuota disponible no equivale a un pick con valor.
- Los parlays son combinaciones ilustrativas; no se modelan correlaciones ni probabilidades conjuntas.
- Resultados/ROI aún requieren liquidación verificada y registro de stakes.

## Variables de entorno en Railway
- `TELEGRAM_BOT_TOKEN`: token de BotFather.
- `ODDS_API_KEY`: clave de The Odds API.
- `TELEGRAM_CHAT_ID`: ID del chat que recibirá los mensajes programados.
- `TZ=America/El_Salvador`
- `DAILY_PICKS_HOUR=7`
- `UPDATE_HOUR=15`

No subas `.env` ni tokens a GitHub.

## Ejecutar localmente
```bash
pip install -r requirements.txt
python main.py
```

## Comandos
`/start`, `/help`, `/picks`, `/futbol`, `/nba`, `/nfl`, `/parlays`,
`/live`, `/resultados`, `/roi`, `/analizar <equipo>`

## Despliegue
Conecta este repositorio a Railway y configura las variables en la pestaña Variables.
El proceso de arranque está definido en `Procfile`.
