# Función
def inline_keyboard(dictionary):  # Crea un inline_keyboard a partir de un diccionario
    lista = []
    keys = list(dictionary.keys())
    # Creación del vector lista a partir del diccionario
    for i in range(len(dictionary)):
        lista.append([{"text": keys[i], "callback_data": keys[i]}])
    # Creación del inline_keyboard a partir de la lista
    keyboard = {"inline_keyboard": lista}
    return keyboard
