import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu bot de recordatorios.\n"
        "Usa /recordar 10 Llamar al doctor\n"
        "para que te recuerde algo en 10 minutos."
    )

async def recordar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        minutos = int(context.args[0])
        mensaje = " ".join(context.args[1:])
        await update.message.reply_text(f"Listo, te recuerdo en {minutos} minutos: {mensaje}")

        async def enviar_recordatorio(context: ContextTypes.DEFAULT_TYPE):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Recordatorio: {mensaje}"
            )

        context.job_queue.run_once(enviar_recordatorio, minutos * 60)
    except (IndexError, ValueError):
        await update.message.reply_text("Uso correcto: /recordar 10 Llamar al doctor")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("recordar", recordar))

print("Bot corriendo...")
app.run_polling()