# Clase
class User:

    def __init__(self, updates):
        for item in updates:
            self.update_id = item["update_id"]
            # El mensaje puede venir en diferentes formatos según el tipo de mensaje que sea
            try:    # Mensaje de texto normal
                self.from_ = item["message"]["from"]["id"]
                self.chat_name = str(item["message"]["from"]["first_name"])
                self.date = item["message"]["date"]
                self.message_text = str(item["message"]["text"])
                self.language = str(item["message"]["from"]["language_code"])
                try:
                    self.chat_username = str(item["message"]["from"]["username"])
                except:
                    self.chat_username = None
                self.type_chat = item["message"]["chat"]["type"]
                self.type_message = "message"
            except:
                try:    # Mensaje que viene de un inline_keyboard
                    self.from_ = item["callback_query"]["message"]["chat"]["id"]
                    self.chat_name = str(item["callback_query"]["from"]["first_name"])
                    self.date = item["callback_query"]["message"]["date"]
                    self.message_text = str(item["callback_query"]["data"])
                    self.language = str(item["callback_query"]["from"]["language_code"])
                    try:
                        self.chat_username = str(item["callback_query"]["message"]["from"]["username"])
                    except:
                        self.chat_username = None
                    self.type_chat = item["callback_query"]["message"]["chat"]["type"]
                    self.type_message = "callback_query"
                except:  # Los siguientes tipos de mensajes son inútiles para el Bot actualmente
                    # Únicamente se necesita del último except:, pero se deja el resto de tipos para futuras ampliaciones del bot
                    try:    # Mensaje editado
                        self.from_ = item["edited_message"]["chat"]["id"]
                        self.chat_name = str(item["edited_message"]["from"]["first_name"])
                        self.date = item["edited_message"]["date"]
                        self.message_text = str(item["edited_message"]["text"])
                        self.language = str(item["edited_message"]["from"]["language_code"])
                        try:
                            self.chat_username = str(item["edited_message"]["from"]["username"])
                        except:
                            self.chat_username = None
                        self.type_chat = item["edited_message"]["chat"]["type"]
                        self.type_message = "edited_message"
                    except:
                        try:    # Foto
                            self.from_ = item["message"]["from"]["id"]
                            self.chat_name = str(item["message"]["from"]["first_name"])
                            self.date = item["message"]["date"]
                            self.message_text = str(item["message"]["photo"][2]["file_id"])
                            self.language = str(item["message"]["from"]["language_code"])
                            try:
                                self.chat_username = str(item["message"]["from"]["username"])
                            except:
                                self.chat_username = None
                            self.type_chat = item["message"]["chat"]["type"]
                            self.type_message = "photo"
                        except:
                            try:    # Video
                                self.from_ = item["message"]["from"]["id"]
                                self.chat_name = str(item["message"]["from"]["first_name"])
                                self.date = item["message"]["date"]
                                self.message_text = str(item["message"]["video_note"]["file_id"])
                                self.language = str(item["message"]["from"]["language_code"])
                                try:
                                    self.chat_username = str(item["message"]["from"]["username"])
                                except:
                                    self.chat_username = None
                                self.type_chat = item["message"]["chat"]["type"]
                                self.type_message = "video"
                            except:
                                try:    # Gif
                                    self.from_ = item["message"]["from"]["id"]
                                    self.chat_name = str(item["message"]["from"]["first_name"])
                                    self.date = item["message"]["date"]
                                    self.message_text = str(item["message"]["animation"]["file_id"])
                                    self.language = str(item["message"]["from"]["language_code"])
                                    try:
                                        self.chat_username = str(item["message"]["from"]["username"])
                                    except:
                                        self.chat_username = None
                                    self.type_chat = item["message"]["chat"]["type"]
                                    self.type_message = "animation"
                                except:
                                    try:    # Documento
                                        self.from_ = item["message"]["from"]["id"]
                                        self.chat_name = str(item["message"]["from"]["first_name"])
                                        self.date = item["message"]["date"]
                                        self.message_text = str(item["message"]["document"]["file_id"])
                                        self.language = str(item["message"]["from"]["language_code"])
                                        try:
                                            self.chat_username = str(item["message"]["from"]["username"])
                                        except:
                                            self.chat_username = None
                                        self.type_chat = item["message"]["chat"]["type"]
                                        self.type_message = "document"
                                    except:
                                        try:  # Sticker
                                            self.from_ = item["message"]["from"]["id"]
                                            self.chat_name = str(item["message"]["from"]["first_name"])
                                            self.date = item["message"]["date"]
                                            self.message_text = str(item["message"]["sticker"]["file_id"])
                                            self.language = str(item["message"]["from"]["language_code"])
                                            try:
                                                self.chat_username = str(item["message"]["from"]["username"])
                                            except:
                                                self.chat_username = None
                                            self.type_chat = item["message"]["chat"]["type"]
                                            self.type_message = "sticker"
                                        except:
                                            try:    # Mensaje de voz
                                                self.from_ = item["message"]["from"]["id"]
                                                self.chat_name = str(item["message"]["from"]["first_name"])
                                                self.date = item["message"]["date"]
                                                self.message_text = str(item["message"]["voice"]["file_id"])
                                                self.language = str(item["message"]["from"]["language_code"])
                                                try:
                                                    self.chat_username = str(item["message"]["from"]["username"])
                                                except:
                                                    self.chat_username = None
                                                self.type_chat = item["message"]["chat"]["type"]
                                                self.type_message = "voice"
                                            except:
                                                try:  # Ubicación
                                                    self.from_ = item["message"]["from"]["id"]
                                                    self.chat_name = str(item["message"]["from"]["first_name"])
                                                    self.date = item["message"]["date"]
                                                    self.message_text = [item["message"]["location"]["latitude"],
                                                                         item["message"]["location"]["longitude"]]
                                                    self.language = str(item["message"]["from"]["language_code"])
                                                    try:
                                                        self.chat_username = str(item["message"]["from"]["username"])
                                                    except:
                                                        self.chat_username = None
                                                    self.type_chat = item["message"]["chat"]["type"]
                                                    self.type_message = "location"
                                                except:
                                                    try:  # Ubicación en tiempo real
                                                        self.from_ = item["edited_message"]["from"]["id"]
                                                        self.chat_name = str(item["edited_message"]["from"]["first_name"])
                                                        self.date = item["edited_message"]["date"]
                                                        self.message_text = [item["edited_message"]["location"]["latitude"],
                                                                             item["edited_message"]["location"]["longitude"]]
                                                        self.language = str(item["edited_message"]["from"]["language_code"])
                                                        try:
                                                            self.chat_username = str(
                                                                item["edited_message"]["from"]["username"])
                                                        except:
                                                            self.chat_username = None
                                                        self.type_chat = item["edited_message"]["chat"]["type"]
                                                        self.type_message = "live_location"
                                                    except:
                                                        try:  # Encuesta
                                                            self.from_ = item["message"]["from"]["id"]
                                                            self.chat_name = str(
                                                                item["message"]["from"]["first_name"])
                                                            self.date = item["message"]["date"]
                                                            self.message_text = item["message"]["poll"]["id"]
                                                            self.language = str(
                                                                item["message"]["from"]["language_code"])
                                                            try:
                                                                self.chat_username = str(
                                                                    item["message"]["from"]["username"])
                                                            except:
                                                                self.chat_username = None
                                                            self.type_chat = item["message"]["chat"]["type"]
                                                            self.type_message = "poll"
                                                        except:
                                                            try:  # Música
                                                                self.from_ = item["message"]["from"]["id"]
                                                                self.chat_name = str(
                                                                    item["message"]["from"]["first_name"])
                                                                self.date = item["message"]["date"]
                                                                self.message_text = item["message"]["audio"]["file_id"]
                                                                self.language = str(
                                                                    item["message"]["from"]["language_code"])
                                                                try:
                                                                    self.chat_username = str(
                                                                        item["message"]["from"]["username"])
                                                                except:
                                                                    self.chat_username = None
                                                                self.type_chat = item["message"]["chat"]["type"]
                                                                self.type_message = "audio"
                                                            except:
                                                                try:  # Contacto
                                                                    self.from_ = item["message"]["from"]["id"]
                                                                    self.chat_name = str(
                                                                        item["message"]["from"]["first_name"])
                                                                    self.date = item["message"]["date"]
                                                                    self.message_text = item["message"]["contact"]["vcard"]
                                                                    self.language = str(
                                                                        item["message"]["from"]["language_code"])
                                                                    try:
                                                                        self.chat_username = str(
                                                                            item["message"]["from"]["username"])
                                                                    except:
                                                                        self.chat_username = None
                                                                    self.type_chat = item["message"]["chat"][
                                                                        "type"]
                                                                    self.type_message = "contact"
                                                                except: # Para cualquier otra cosa
                                                                    self.from_ = ""
                                                                    self.chat_name = ""
                                                                    self.date = ""
                                                                    self.message_text = ""
                                                                    self.language = ""
                                                                    self.chat_username = ""
                                                                    self.type_chat = ""
                                                                    self.type_message = "useless"
