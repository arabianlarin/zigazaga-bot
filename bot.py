from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import charts as ch

import os

TOKEN = os.getenv('8007828935:AAHq54YtPrLmJRxoFE7ZS92WAW_z_3icGs4')
print("Render TELEGRAM_TOKEN:", TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send Player1, Player2 to compare.')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "," not in text.lower():
        return await update.message.reply_text("Use format: Player1, Player2")
    p1, p2 = [x.strip() for x in text.split(",")]
    result = ch.chart_player_comparison_att(p1, p2)
    await update.message.reply_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        url_path=TOKEN,
        #webhook_url=f"https://YOUR_CLOUD_RUN_URL/{TOKEN}"
    )
