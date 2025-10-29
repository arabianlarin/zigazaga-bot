from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import charts as ch

import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
print("Render TELEGRAM_TOKEN:", TELEGRAM_TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi!')

async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /compare player1 player2")
        return

    player1, player2 = context.args[0], context.args[1]
    await update.message.reply_text(f"Comparing {player1} vs {player2}...")

    try:
        chart_path = ch.chart_player_comparison_att(player1, player2)
        await update.message.reply_photo(photo=open(chart_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("compare", compare))
#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://zigazaga-bot.onrender.com/{TELEGRAM_TOKEN}"
    )
