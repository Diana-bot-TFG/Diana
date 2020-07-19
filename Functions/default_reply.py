# Módulos
from Python_server.initialization import bot


# Función
def default_reply(usuario):  # Respuesta por defecto
    if usuario['language'] == "es":
        bot.send_message(f"¿{usuario['name']}, qué quiere que haga ahora? Recuerde usar los comandos, si tiene alguna "
                         f"duda pulse /help", usuario['id'])

    else:
        bot.send_message(f"{usuario['name']}, what do you want me to do now? Remember to use the commands, if you "
                         f"have any doubt press /help", usuario['id'])
