import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
TOKEN_EXPIRY_MINS = int(os.getenv('TOKEN_EXPIRY_MINS', 30))