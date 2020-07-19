# Librerías
import requests
import json
import configparser as cfg


# Clase
class telegram_bot():

    def __init__(self, config):
        self.token = self.read_token(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    # Función que sirve para ver si ha habido un mensaje nuevo al bot en Telegram
    def get_updates(self, offset=None):
        url = self.base + "getUpdates"
        if offset:
            url = url + "?offset={}&timeout=100&allowed_updates=[“message”]".format(offset+1)
        r = requests.get(url)
        return json.loads(r.content)

    # Función que envía un mensaje o un menú al usuario
    def send_message(self, msg, chat_id, reply_keyboard=None):
        if reply_keyboard is not None:
            url = self.base + "sendMessage?chat_id={}&text={}&parse_mode={}&reply_markup={}".format(chat_id, msg, "Markdown", json.dumps(reply_keyboard))
        else:
            url = self.base + "sendMessage?chat_id={}&text={}&parse_mode={}".format(chat_id, msg, "Markdown")
        if msg is not None:
            requests.get(url)

    # Función que lee del config.cfg la contraseña del Totem
    def read_token(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('token', 'token_telegram')