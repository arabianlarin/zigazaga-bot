from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import charts as ch

import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
print("Render TELEGRAM_TOKEN:", TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Hi!
    /compare_att - Compare attacking stats
    /compare_def - Compare defending stats
    /compare_gk - Compare GK stats
    ''')

async def compare_att(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/compare_att", "").strip()

    # Split by comma and clean whitespace
    players = [p.strip() for p in text.split(",") if p.strip()]

    if len(players) < 2:
        await update.message.reply_text("Usage: /compare_att player1, player2")
        return

    player1, player2 = players[0], players[1]
    await update.message.reply_text(f"Comparing {player1} vs {player2}...")

    try:
        chart_path = ch.chart_player_comparison_att(player1, player2)
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: type names exactly as you see in your FPL squad")

async def compare_def(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/compare_def", "").strip()

    # Split by comma and clean whitespace
    players = [p.strip() for p in text.split(",") if p.strip()]

    if len(players) < 2:
        await update.message.reply_text("Usage: /compare_def player1, player2")
        return

    player1, player2 = players[0], players[1]
    await update.message.reply_text(f"Comparing {player1} vs {player2}...")

    try:
        chart_path = ch.chart_player_comparison_def(player1, player2)
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: type names exactly as you see in your FPL squad")

async def compare_gk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/compare_gk", "").strip()

    # Split by comma and clean whitespace
    players = [p.strip() for p in text.split(",") if p.strip()]

    if len(players) < 2:
        await update.message.reply_text("Usage: /compare_gk player1, player2")
        return

    player1, player2 = players[0], players[1]
    await update.message.reply_text(f"Comparing {player1} vs {player2}...")

    try:
        chart_path = ch.chart_player_comparison_gk(player1, player2)
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: type names exactly as you see in your FPL squad")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("compare_att", compare_att))
app.add_handler(CommandHandler("compare_def", compare_def))
app.add_handler(CommandHandler("compare_gk", compare_gk))
#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://zigazaga-bot.onrender.com/{TELEGRAM_TOKEN}"
    )
