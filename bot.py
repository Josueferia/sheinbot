import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

TOKEN = "7459460142:AAHBe93qgXCwniLC4yXDcYP6l8t-A_2V0ac"
ADMIN_ID = 991273718  # Reemplaza con tu ID de usuario en Telegram para enviarte los mensajes modificados

def get_bin_info(bin_number):
    """Consulta la API de BinList y, si no encuentra el BIN, consulta una alternativa"""
    url_binlist = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}

    try:
        # Consultar en BinList
        response = requests.get(url_binlist, headers=headers)
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Desconocido")
            country = data.get("country", {}).get("name", "Desconocido")
            scheme = data.get("scheme", "Desconocido")
            card_type = data.get("type", "Desconocido")
            brand = data.get("brand", "Desconocido")

            return f"🏦 <b>Banco:</b> {bank}\n🌍 <b>País:</b> {country}\n💳 <b>Tipo de tarjeta:</b> {card_type}\n🎨 <b>Marca:</b> {brand}\n🔄 <b>Esquema:</b> {scheme}"
        else:
            print(f"⚠️ BinList no tiene información para el BIN {bin_number}.")
            return get_bin_info_alternative(bin_number)

    except Exception as e:
        print(f"⚠️ Error con BinList: {e}, probando otra fuente.")
        return get_bin_info_alternative(bin_number)

def get_bin_info_alternative(bin_number):
    """Consulta una API alternativa de BINs"""
    api_key = "TU_CLAVE_DE_API"  # Reemplaza con tu API key de la fuente alternativa
    url_alternative = f"https://bins.antipublic.cc/bins/{bin_number}"

    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url_alternative, headers=headers)
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", "Desconocido")
            country = data.get("country", "Desconocido")
            type_card = data.get("type", "Desconocido")

            return f"🏦 <b>Banco:</b> {bank}\n🌍 <b>País:</b> {country}\n💳 <b>Tipo de tarjeta:</b> {type_card}"
        else:
            return "⚠️ No se encontró información del BIN en la fuente alternativa."

    except Exception as e:
        print(f"⚠️ Error con la fuente alternativa: {e}")
        return "⚠️ No se pudo obtener la información del BIN."

async def handle_message(update: Update, context):
    """Maneja los mensajes recibidos y modifica los que contienen 'ADD A NEW CARD'"""
    message_text = update.message.text
    if "ADD A NEW CARD" in message_text:
        modified_message = message_text.replace("ADD A NEW CARD", "<b>MALA</b>")
        bin_number = message_text.split('-')[0]
        bin_info = get_bin_info(bin_number)
        modified_message += f"\n{bin_info}"

        try:
            # Enviar mensaje modificado al admin
            await context.bot.send_message(chat_id=ADMIN_ID, text=modified_message, parse_mode="HTML")
            print(f"📤 Mensaje enviado al admin: {modified_message}")
        except Exception as e:
            print(f"⚠️ Error al enviar mensaje al admin: {e}")
    else:
        print(f"📩 Mensaje recibido: {message_text}")

def main():
    """Inicia la aplicación de Telegram y configura el webhook"""
    app = Application.builder().token(TOKEN).build()

    # Configura el webhook con la URL pública de Railway
    app.run_webhook(listen="0.0.0.0", port=8080, url_path=TOKEN, webhook_url="https://sheinbot-production.up.railway.app/")

    # Agregar un handler para mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ejecuta el bot
    print("✅ Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()

