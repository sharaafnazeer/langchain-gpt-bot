from whatsapp_api_client_python import API
import os
from dotenv import load_dotenv

load_dotenv()

greenAPI = API.GreenApi(os.getenv("ID_INSTANCE"), os.getenv("API_TOKEN_INSTANCE"))

def send_message(to: str, message: str) : 
    result = greenAPI.sending.sendMessage(to, message)
    return result.data