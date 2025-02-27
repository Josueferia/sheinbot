import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

TOKEN = "7459460142:AAHBe93qgXCwniLC4yXDcYP6l8t-A_2V0ac"

async def detect_message(update: Update, context: CallbackContext) -> None:
    """Detecta si el mensaje es 'ADD A NEW CARD' y lo edita"""
    if update.message.text == "ADD A NEW CARD":
        # Enviar el mensaje inicial
        message = await update.message.reply_text("Procesando...")
        await asyncio.sleep(2)  # Espera 2 segundos antes de editar

        # Editar el mensaje con "MALA" en rojo usando MarkdownV2
        await message.edit_text("🔴 *MALA*", parse_mode="MarkdownV2")

def main():
    app = Application.builder().token(TOKEN).build()

    # Manejar todos los mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_message))

    print("Bot en ejecución...")
    app.run_polling()

if __name__ == '__main__':
    main()


