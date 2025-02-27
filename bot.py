import asyncio
import requests
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

TOKEN = "7459460142:AAHBe93qgXCwniLC4yXDcYP6l8t-A_2V0ac"
ADMIN_ID = 991273718  # Reemplaza con tu ID de usuario en Telegram

def get_bin_info(bin_number):
    """Consulta la API de BinList y, si no encuentra el BIN, usa otra API alternativa"""
    url_binlist = f"https://lookup.binlist.net/{bin_number}"
    headers = {"Accept-Version": "3"}

    try:
        # Consultar en BinList
        response = requests.get(url_binlist, headers=headers)
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Desconocido")
            country = data.get("country", {}).get("name", "Desconocido")
            scheme = data.get("scheme", "Desconocido").capitalize()
            card_type = data.get("type", "Desconocido").capitalize()
            brand = data.get("brand", "Desconocido")

            return f"🏦 <b>Banco:</b> {bank}\n🌍 <b>País:</b> {country}\n💳 <b>Tipo:</b> {scheme} - {brand} ({card_type})"
        
        else:
            print(f"⚠️ BinList no tiene información para el BIN {bin_number}, probando otra API...")
            return get_bin_info_alternative(bin_number)

    except Exception as e:
        print(f"⚠️ Error con BinList: {e}, probando otra API...")
        return get_bin_info_alternative(bin_number)

def get_bin_info_alternative(bin_number):
    """Consulta una API alternativa de BINs"""
    api_key = "TU_CLAVE_DE_API"  # Reemplaza con tu API Key si es necesario
    url_alternative = f"https://bins.antipublic.cc/bins/{bin_number}"

    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url_alternative, headers=headers)
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", "Desconocido")
            country = data.get("country", "Desconocido")
            type_card = data.get("type", "Desconocido")

            return f"🏦 <b>Banco:</b> {bank}\n🌍 <b>País:</b> {country}\n💳 <b>Tipo:</b> {type_card}"
        
        else:
            return "⚠️ No se encontró información del BIN en ninguna API."
    
    except Exception as e:
        return f"⚠️ Error al consultar API alternativa: {str(e)}"

async def detect_message(update: Update, context: CallbackContext) -> None:
    """Detecta si el mensaje contiene 'ADD A NEW CARD', lo modifica y envía info del BIN"""
    message_text = update.message.text
    print(f"📩 Mensaje recibido: {message_text}")  # Para depuración

    if "ADD A NEW CARD" in message_text:
        # Extraer el BIN (los primeros 6 dígitos antes del primer "-")
        bin_number = message_text.split("-")[0][:6]

        # Obtener información del BIN
        bin_info = get_bin_info(bin_number)

        # Modificar el mensaje reemplazando "ADD A NEW CARD" con "MALA"
        modified_text = message_text.replace("ADD A NEW CARD", "<b>🔴 MALA</b>")

        # Crear el mensaje final con la info del BIN
        final_message = f"""
📢 <b>Mensaje recibido:</b>\n{modified_text}\n\n🆔 <b>BIN Detectado:</b> {bin_number}\n{bin_info}
        """.strip()

        # Depuración antes de enviar el mensaje
        print("📤 Enviando mensaje privado al admin...")

        # Enviar el mensaje corregido en privado al admin
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=final_message, parse_mode="HTML")
            print("✅ Mensaje enviado al admin.")
        except Exception as e:
            print(f"⚠️ Error al enviar mensaje al admin: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()

    # Manejar todos los mensajes de texto en grupos
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_message))

    print("✅ Bot en ejecución...")
    # Cambia de run_polling a run_webhook
    app.run_webhook(listen="0.0.0.0", port=8080, url_path=TOKEN)

if __name__ == '__main__':
    main()

