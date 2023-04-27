from src.app import app
from helper.green_api import receive_message
import os
from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    app.secret_key = os.getenv("APP_SECRET")
    app.run(host='0.0.0.0', port=5000, debug=True)
    # receive_message()
