# Librerías
from currency_converter import CurrencyConverter
from pymongo import MongoClient

# Módulos
from Telegram_server.bot import telegram_bot

# Telegram
bot = telegram_bot('config.cfg')

# Divisas
c = CurrencyConverter()

# Base de datos
client = MongoClient('localhost', 27017)
db = client.diana
cluster = db.diana_usuarios
