# Librerías
import json
import time

# Archivos
from Telegram_server.user import User
from Python_server.initialization import bot, c, cluster

# Diccionarios
from Dictionaries.dictionaries import paises, languages, divisas, divisas_simbolo

# Menús
from Dictionaries.menus import menu_price_range, menu_shops, menu_tracking

# Funciones
from Functions.check import check
from Functions.default_reply import default_reply
from Functions.inline_keyboard import inline_keyboard
from Functions.search import search
from Functions.state import state
from Functions.tracking import tracking
from Functions.email import send_email

# --------------------------------------------------------------------------------------------------

# Main
update_id = None

while True:
    # Mira a ver si hay un mensaje nuevo
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]

    # Actualiza los tracking de todos los usuarios a las 2:30am (para hacerlo a una hora con poca carga en el bot)
    if time.strftime("%X") == "02:30:00":
        tracking()

    # Se entra en el if si se recibe un mensaje
    if updates:
        print(json.dumps(updates, indent=2, sort_keys=True))
        user = User(updates)
        update_id = user.update_id

        # Base de datos
        if user.from_ != "":  # Si no hay id del usuario es porque es un mensaje no analizable (fotos, vídeos, etc)
            if cluster.find_one({'id': user.from_}):  # Comprobación de si el usuario está en la base de datos
                usuario = cluster.find_one({'id': user.from_})  # Si está en la base de datos se carga su información
            else:
                # Comprobación de si se tiene el idioma del usuario, si no se le aplica el inglés
                if user.language in languages.values():
                    pass
                else:
                    user.language = "en"
                # Definición del usuario, en caso de no estar previamente en la base de datos
                usuario = {
                    'id': user.from_,
                    'name': user.chat_name,
                    'username': user.chat_username,
                    'language': user.language,
                    'country': paises["Spain"],
                    'currency': divisas["EUR"],
                    'range':
                        {
                            'min': 0,
                            'max': 1000
                        },
                    'shops':
                        {
                            'Ebay': True,
                            'Gearbest': True,
                            'Banggood': True,
                            'Links': True
                        },
                    'state_machine':
                        {
                            'search': 0,
                            'price_range': 0,
                            'shops': 0,
                            'tracking': 0,
                            'country': 0,
                            'language': 0,
                            'currency': 0
                        }
                }
                # Inserción del usuario en la base de datos
                cluster.insert_one(usuario)

        # Se entra al if si es un mensaje escrito o de menú y viene de un chat privado
        if user.type_chat == "private" and user.type_message == "message" or user.type_message == "callback_query":
            try:
                # Primera máquina de estados
                if user.message_text == "/start" or user.message_text == "/help":
                    # Se distingue si el idioma del usuario es español o inglés, esto se hará continuamente durante el código
                    if usuario['language'] == "es":
                        bot.send_message(
                            f"Hola {usuario['name']}, me llamo Diana, soy un Bot orientado a las compras en Internet, "
                            "puedes usarme para buscar algo que necesites"
                            "\n\n*Comandos*" +
                            "\n/search - busca un producto por su nombre" +
                            "\n/price\_range - elige el mínimo y máximo precio (inicialmente 0-1000€)" +
                            "\n/shops - selecciona las tiendas que quieres usar" +
                            "\n/tracking - muestra los productos en lista de seguimiento" +
                            "\n/country - cambia el país de búsqueda" +
                            "\n/language - cambia el idioma" +
                            "\n/currency - cambia la divisa" +
                            "\n/help - muestra todos los comandos" +
                            "\n/contact - envía un mensaje al administrador" +
                            "\n/cancel - cancela la última orden", usuario['id'])
                    else:
                        bot.send_message(
                            f"Hello {usuario['name']}, my name is Diana, I am a Bot oriented to Internet purchases, "
                            "you can use me to find something you need"
                            "\n\n*Commands*" +
                            "\n/search - search for a product by name" +
                            "\n/price\_range - select the minimum and maximum price (inicially 0-1000€)" +
                            "\n/shops - select which shops you want to use" +
                            "\n/tracking - show the tracking list" +
                            "\n/country - change country" +
                            "\n/language - change language" +
                            "\n/currency - change currency" +
                            "\n/help - show all commands" +
                            "\n/contact - send a message to the administrator" +
                            "\n/cancel - cancel the last order", usuario['id'])

                elif user.message_text == "/search":

                    if usuario['language'] == "es":
                        bot.send_message("Introduce el nombre del producto que quieras", usuario['id'])
                    else:
                        bot.send_message("Send the name of the product you want", usuario['id'])

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 1, 0, 0, 0, 0, 0, 0, 0)

                elif user.message_text == "/price_range":

                    if usuario['language'] == "es":
                        bot.send_message("*¿Qué desea cambiar?*", usuario['id'], inline_keyboard(menu_price_range))
                    else:
                        bot.send_message("*What do you want to change?*", usuario['id'],
                                         inline_keyboard(menu_price_range))

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 1, 0, 0, 0, 0, 0, 0)

                elif user.message_text == "/shops":

                    if usuario['language'] == "es":
                        bot.send_message("*Seleccione las tiendas que quiera usar y pulse Finish*", usuario['id'],
                                         inline_keyboard(menu_shops))
                    else:
                        bot.send_message("*Select the shops you want to use and press Finish*", usuario['id'],
                                         inline_keyboard(menu_shops))

                    # Se ponen todas las tiendas en OFF
                    cluster.update_one(
                        {
                            'id': usuario['id']
                        },
                        {
                            '$set':
                                {
                                    'shops.Ebay': False,
                                    'shops.Gearbest': False,
                                    'shops.Banggood': False,
                                    'shops.Links': False
                                }
                        }
                    )

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 1, 0, 0, 0, 0, 0)

                elif user.message_text == "/tracking":

                    if usuario['language'] == "es":
                        bot.send_message("*Elija una opcion*:", usuario['id'], inline_keyboard(menu_tracking))
                    else:
                        bot.send_message("*Select an option*:", usuario['id'], inline_keyboard(menu_tracking))

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 1, 0, 0, 0, 0)

                elif user.message_text == "/country":

                    if usuario['language'] == "es":
                        bot.send_message("*Elija su pais*", usuario['id'], inline_keyboard(paises))
                    else:
                        bot.send_message("*Select your country*", usuario['id'], inline_keyboard(paises))

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 0, 1, 0, 0, 0)

                elif user.message_text == "/language":

                    if usuario['language'] == "es":
                        bot.send_message("*Elija su idioma*", usuario['id'], inline_keyboard(languages))
                    else:
                        bot.send_message("*Select your language*", usuario['id'], inline_keyboard(languages))

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 0, 0, 1, 0, 0)

                elif user.message_text == "/currency":

                    if usuario['language'] == "es":
                        bot.send_message("*Elija su moneda*", usuario['id'], inline_keyboard(divisas))
                    else:
                        bot.send_message("*Select your currency*", usuario['id'], inline_keyboard(divisas))

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 0, 0, 0, 1, 0)

                elif user.message_text == "/contact":
                    if usuario['language'] == "es":
                        bot.send_message("Escriba el mensaje a enviar", usuario['id'])
                    else:
                        bot.send_message("Write the message to send", usuario['id'])

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 1)

                elif user.message_text == "/cancel":

                    if usuario['language'] == "es":
                        bot.send_message("Operacion cancelada", usuario['id'])
                    else:
                        bot.send_message("Operation cancelled", usuario['id'])

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                # Segunda máquina de estados
                elif usuario['state_machine']['search'] == 1:

                    if usuario['language'] == "es":
                        bot.send_message("Buscando...", usuario['id'])
                    else:
                        bot.send_message("Searching...", usuario['id'])
                    # Búsqueda
                    search(user.message_text, usuario['shops']['Ebay'], usuario['shops']['Gearbest'],
                           usuario['shops']['Banggood'], usuario['shops']['Links'], usuario)
                    # No se sale de este estado, para poder buscar varias cosas seguidas

                elif usuario['state_machine']['price_range'] == 1:

                    if user.message_text == "Price Min":

                        if usuario['language'] == "es":
                            bot.send_message("Introduzca un precio mínimo", usuario['id'])
                        else:
                            bot.send_message("Enter the minimum price", usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 2, 0, 0, 0, 0, 0, 0)

                    elif user.message_text == "Price Max":

                        if usuario['language'] == "es":
                            bot.send_message("Introduzca un precio máximo", usuario['id'])
                        else:
                            bot.send_message("Enter the maximum price", usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 3, 0, 0, 0, 0, 0, 0)

                    elif user.message_text == "Finish":

                        if usuario['language'] == "es":
                            bot.send_message(
                                f"*Precio Min:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}\n"
                                f"*Precio Max:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                usuario['id'])
                        else:
                            bot.send_message(
                                f"*Precio Min:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}\n"
                                f"*Precio Max:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                elif usuario['state_machine']['price_range'] == 2:

                    try:
                        float(user.message_text)
                        # Insertamos el nuevo precio mínimo
                        cluster.update_one({'id': usuario['id']}, {'$set': {'range.min': user.message_text}})

                        # Descarga del nuevo usuario con el nuevo precio mínimo
                        usuario = cluster.find_one({'id': usuario['id']})

                        if usuario['language'] == "es":
                            bot.send_message(
                                f"*Precio mínimo:*  {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}",
                                usuario['id'])
                        else:
                            bot.send_message(
                                f"*Minimum Price:*  {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}",
                                usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 1, 0, 0, 0, 0, 0, 0)

                        if usuario['language'] == "es":
                            bot.send_message("*¿Qué desea cambiar?*", usuario['id'], inline_keyboard(menu_price_range))
                        else:
                            bot.send_message(
                                "*What do you want to change?*", usuario['id'],
                                inline_keyboard(menu_price_range))

                    except:
                        if user.message_text == "Finish":
                            if usuario['language'] == "es":
                                bot.send_message(
                                    f"*Precio Min:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}"
                                    f"\n*Precio Max:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                    usuario['id'])
                            else:
                                bot.send_message(
                                    f"*Min Price:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}"
                                    f"\n*Max Price:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                    usuario['id'])

                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                        else:
                            if usuario['language'] == "es":
                                bot.send_message(
                                    "Ha ocurrido un error, escriba nuevamente el precio mínimo "
                                    "(use el punto para los decimales, no la coma)", usuario['id'])
                            else:
                                bot.send_message(
                                    "An error has occurred, write the minimum price again "
                                    "(use the decimal point for not comma)", usuario['id'])

                elif usuario['state_machine']['price_range'] == 3:
                    try:
                        float(user.message_text)
                        # Insertamos el nuevo precio máximo
                        cluster.update_one({'id': usuario['id']}, {'$set': {'range.max': user.message_text}})

                        # Descarga del nuevo usuario con el nuevo precio máximo
                        usuario = cluster.find_one({'id': usuario['id']})

                        if usuario['language'] == "es":
                            bot.send_message(
                                f"*Precio máximo:*  {usuario['range']['max']} "
                                f"{divisas_simbolo[usuario['currency']]}",
                                usuario['id'])
                        else:
                            bot.send_message(
                                f"*Maximum price:*  {usuario['range']['max']} "
                                f"{divisas_simbolo[usuario['currency']]}",
                                usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 1, 0, 0, 0, 0, 0, 0)

                        if usuario['language'] == "es":
                            bot.send_message("*¿Qué desea cambiar?*", usuario['id'], inline_keyboard(menu_price_range))
                        else:
                            bot.send_message(
                                "*What do you want to change?*", usuario['id'], inline_keyboard(menu_price_range))

                    except:
                        if user.message_text == "Finish":
                            if usuario['language'] == "es":
                                bot.send_message(
                                    f"*Precio Min:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}"
                                    f"\n*Precio Max:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                    usuario['id'])
                            else:
                                bot.send_message(
                                    f"*Min Price:* {usuario['range']['min']} {divisas_simbolo[usuario['currency']]}"
                                    f"\n*Max Price:* {usuario['range']['max']} {divisas_simbolo[usuario['currency']]}",
                                    usuario['id'])

                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                        else:
                            if usuario['language'] == "es":
                                bot.send_message(
                                    "Ha ocurrido un error, escriba nuevamente el precio máximo "
                                    "(use el punto para los decimales, no la coma)", usuario['id'])
                            else:
                                bot.send_message(
                                    "An error has occurred, write the maximum price again "
                                    "(use the decimal point for not comma)", usuario['id'])

                elif usuario['state_machine']['shops'] == 1:

                    if user.message_text == 'Ebay':

                        if usuario['language'] == "es":
                            bot.send_message("*Ebay activa*", usuario['id'])
                        else:
                            bot.send_message("*Ebay active*", usuario['id'])

                        # Activación de Ebay
                        cluster.update_one({'id': usuario['id']}, {'$set': {'shops.Ebay': True}})

                    elif user.message_text == 'Gearbest':

                        if usuario['language'] == "es":
                            bot.send_message("*Gearbest activa*", usuario['id'])
                        else:
                            bot.send_message("*Gearbest active*", usuario['id'])

                        # Activación de Gearbest
                        cluster.update_one({'id': usuario['id']}, {'$set': {'shops.Gearbest': True}})

                    elif user.message_text == 'Banggood':

                        if usuario['language'] == "es":
                            bot.send_message("*Banggood activa*", usuario['id'])
                        else:
                            bot.send_message("*Banggood active*", usuario['id'])

                        # Activación de Banggood
                        cluster.update_one({'id': usuario['id']}, {'$set': {'shops.Banggood': True}})

                    elif user.message_text == "Links":

                        if usuario['language'] == "es":
                            bot.send_message("*Links activos*", usuario['id'])
                        else:
                            bot.send_message("*Links active*", usuario['id'])

                        # Activación de Links
                        cluster.update_one({'id': usuario['id']}, {'$set': {'shops.Links': True}})

                    elif user.message_text == "↩️ Finish":
                        # Descarga del nuevo usuario
                        usuario = cluster.find_one({'id': usuario['id']})
                        if usuario['shops']['Ebay'] == False and usuario['shops']['Gearbest'] == False and \
                                usuario['shops']['Banggood'] == False:
                            if usuario['language'] == "es":
                                bot.send_message("*No ha seleccionado ninguna tienda*", usuario['id'])
                            else:
                                bot.send_message("*You have not seleccted any shop*", usuario['id'])
                        else:
                            default_reply(usuario)
                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                elif usuario['state_machine']['tracking'] == 1:

                    if user.message_text == "My Items":
                        try:
                            if len(usuario['products']) == 0:
                                if usuario['language'] == "es":
                                    bot.send_message("No tiene productos en seguimiento", usuario['id'])
                                else:
                                    bot.send_message("You have no products on tracking", usuario['id'])
                            else:
                                if usuario['language'] == "es":
                                    text = ""
                                    i = 0
                                    for i in range(len(usuario['products'])):
                                        text = text + "\n\n📦*Producto*: {} \n💰*Precio*: {} {} - {} {}".format(
                                            usuario['products'][i]['name_product'],
                                            usuario['products'][i]['price_product_min'],
                                            divisas_simbolo[usuario['currency']],
                                            usuario['products'][i]['price_product_max'],
                                            divisas_simbolo[usuario['currency']])
                                    bot.send_message(text, usuario['id'])
                                else:
                                    text = ""
                                    i = 0
                                    for i in range(len(usuario['products'])):
                                        text = text + "\n\n📦*Item*: {} \n💰*Price*: {} {} - {} {}".format(
                                            usuario['products'][i]['name_product'],
                                            usuario['products'][i]['price_product_min'],
                                            divisas_simbolo[usuario['currency']],
                                            usuario['products'][i]['price_product_max'],
                                            divisas_simbolo[usuario['currency']])
                                    bot.send_message(text, usuario['id'])

                        except:
                            if usuario['language'] == "es":
                                bot.send_message("No tiene productos en seguimiento", usuario['id'])
                            else:
                                bot.send_message("You have no products on tracking", usuario['id'])

                    elif user.message_text == "Add Item":
                        # Borramos lo temporal
                        try:
                            cluster.update_one({'id': usuario['id']}, {"$unset": {"products_temporal": ""}})
                        except:
                            pass

                        if usuario['language'] == "es":
                            bot.send_message("Introduzca el *nombre del producto*", usuario['id'])
                        else:
                            bot.send_message("Enter the *name of the product*", usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 2, 0, 0, 0, 0)

                    elif user.message_text == "Delete Item":
                        diccionario_productos = {}
                        try:
                            i = 0
                            for i in range(len(usuario['products'])):
                                diccionario_productos[usuario['products'][i]['name_product']] = usuario['products'][i]
                                ['name_product']
                            if usuario['language'] == "es":
                                bot.send_message("Seleccione para eliminar", usuario['id'],
                                                 inline_keyboard(diccionario_productos))
                            else:
                                bot.send_message("Select to delete", usuario['id'],
                                                 inline_keyboard(diccionario_productos))

                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 5, 0, 0, 0, 0)

                        except:
                            if usuario['language'] == "es":
                                bot.send_message("No tiene productos en seguimiento", usuario['id'])
                            else:
                                bot.send_message("You have no products on tracking", usuario['id'])

                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 1, 0, 0, 0, 0)

                    elif user.message_text == "Check Items":
                        try:
                            i = 0
                            for i in range(len(usuario['products'])):
                                check(
                                    usuario['id'], usuario['products'][i]['name_product'], usuario['country'],
                                    usuario['currency'], usuario['products'][i]['price_product_min'],
                                    usuario['products'][i]['price_product_max'], usuario['shops']['Ebay'],
                                    usuario['shops']['Gearbest'], usuario['shops']['Banggood'], usuario)

                            if usuario['language'] == "es":
                                bot.send_message("*Elija una opcion*:", usuario['id'], inline_keyboard(menu_tracking))
                            else:
                                bot.send_message("*Select an option*:", usuario['id'], inline_keyboard(menu_tracking))

                        except:
                            if usuario['language'] == "es":
                                bot.send_message("No tiene productos en seguimiento", usuario['id'])
                            else:
                                bot.send_message("You have no products on tracking", usuario['id'])

                            # Actualización del estado de la máquina de estados
                            state(usuario['id'], 0, 0, 0, 1, 0, 0, 0, 0)

                    elif user.message_text == "↩️ Finish":
                        default_reply(usuario)

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                elif usuario['state_machine']['tracking'] == 2:  # Add Item
                    # Insertamos el nombre del item
                    cluster.update_one(
                        {'id': usuario['id']}, {"$set": {'products_temporal.name_product': user.message_text}})

                    if usuario['language'] == "es":
                        bot.send_message("Introduzca un *precio mínimo*", usuario['id'])
                    else:
                        bot.send_message("Enter the *minimum price*", usuario['id'])

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 3, 0, 0, 0, 0)

                elif usuario['state_machine']['tracking'] == 3:  # Add Item
                    try:
                        float(user.message_text)
                        # Insertamos el precio max del item
                        cluster.update_one(
                            {'id': usuario['id']}, {"$set": {'products_temporal.price_product_min': user.message_text}})

                        if usuario['language'] == "es":
                            bot.send_message("Introduzca un *precio máximo*", usuario['id'])
                        else:
                            bot.send_message("Enter the *maximun price*", usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 4, 0, 0, 0, 0)

                    except:
                        if usuario['language'] == "es":
                            bot.send_message(
                                "Ha ocurrido un error, escriba nuevamente el precio mínimo "
                                "(use el punto para los decimales, no la coma)", usuario['id'])
                        else:
                            bot.send_message(
                                "An error has occurred, write the minimum price again "
                                "(use the decimal point for not comma)", usuario['id'])

                elif usuario['state_machine']['tracking'] == 4:  # Add Item
                    try:
                        float(user.message_text)

                        # Insertamos el precio min del item
                        cluster.update_one(
                            {'id': usuario['id']},
                            {"$set": {'products_temporal.price_product_max': user.message_text}})

                        # Descarga del nuevo usuario
                        usuario = cluster.find_one({'id': usuario['id']})

                        # Introducimos finalmente el producto y precios en la base de datos (lo otro era temporal)
                        cluster.update_one(
                            {
                                'id': usuario['id']
                            },
                            {
                                "$addToSet": {'products':
                                    {
                                        'name_product': usuario['products_temporal']['name_product'],
                                        'price_product_min': usuario['products_temporal']['price_product_min'],
                                        'price_product_max': usuario['products_temporal']['price_product_max']
                                    }
                                }
                            }
                        )

                        # Descarga del usuario final
                        usuario = cluster.find_one({'id': usuario['id']})

                        # Mensaje de confirmación
                        if usuario['language'] == "es":
                            bot.send_message(
                                f"Se ha añadido *{usuario['products'][len(usuario['products']) - 1]['name_product']}* entre"
                                f" *{usuario['products'][len(usuario['products']) - 1]['price_product_min']}* "
                                f"{divisas_simbolo[usuario['currency']]} y "
                                f"*{usuario['products'][len(usuario['products']) - 1]['price_product_max']}* "
                                f"{divisas_simbolo[usuario['currency']]}",
                                usuario['id'])
                        else:
                            bot.send_message(
                                f"*{usuario['products'][len(usuario['products']) - 1]['name_product']}* has been added "
                                f" *between {usuario['products'][len(usuario['products']) - 1]['price_product_min']}* "
                                f"{divisas_simbolo[usuario['currency']]} and "
                                f"*{usuario['products'][len(usuario['products']) - 1]['price_product_max']}* "
                                f"{divisas_simbolo[usuario['currency']]}",
                                usuario['id'])

                        # Envío de menu_tracking
                        if usuario['language'] == "es":
                            bot.send_message("*Elija una opcion*:", usuario['id'], inline_keyboard(menu_tracking))
                        else:
                            bot.send_message("*Select an option*:", usuario['id'], inline_keyboard(menu_tracking))

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 1, 0, 0, 0, 0)

                    except:
                        if usuario['language'] == "es":
                            bot.send_message(
                                "Ha ocurrido un error, escriba nuevamente el precio máximo "
                                "(use el punto para los decimales, no la coma)", usuario['id'])
                        else:
                            bot.send_message(
                                "An error has occurred, write the maximum price again "
                                "(use the decimal point for not comma)", usuario['id'])

                elif usuario['state_machine']['tracking'] == 5:  # Delete Item
                    # Se elimina del producto
                    cluster.update_one(
                        {'id': usuario['id']}, {"$pull": {'products': {'name_product': user.message_text}}})

                    # Descarga del nuevo usuario
                    usuario = cluster.find_one({'id': usuario['id']})

                    # Envío del menú tracking
                    if usuario['language'] == "es":
                        bot.send_message("*Elija una opcion*:", usuario['id'], inline_keyboard(menu_tracking))
                    else:
                        bot.send_message("*Select an option*:", usuario['id'], inline_keyboard(menu_tracking))

                        # Se muestra toda la lista
                        try:
                            if usuario['language'] == "es":
                                text = ""
                                i = 0
                                for i in range(len(usuario['products'])):
                                    text = text + "\n\n📦*Producto*: {} \n💰*Precio*: {} {} - {} {}".format(
                                        usuario['products'][i]['name_product'],
                                        usuario['products'][i]['price_product_min'],
                                        divisas_simbolo[usuario['currency']],
                                        usuario['products'][i]['price_product_max'],
                                        divisas_simbolo[usuario['currency']])
                                bot.send_message(text, usuario['id'])
                            else:
                                text = ""
                                i = 0
                                for i in range(len(usuario['products'])):
                                    text = text + "\n\n📦*Item*: {} \n💰*Price*: {} {} - {} {}".format(
                                        usuario['products'][i]['name_product'],
                                        usuario['products'][i]['price_product_min'],
                                        divisas_simbolo[usuario['currency']],
                                        usuario['products'][i]['price_product_max'],
                                        divisas_simbolo[usuario['currency']])
                                bot.send_message(text, usuario['id'])

                        except:
                            if usuario['language'] == "es":
                                bot.send_message("No tiene productos en seguimiento", usuario['id'])
                            else:
                                bot.send_message("You have no products on tracking", usuario['id'])

                    # Actualización del estado de la máquina de estados
                    state(usuario['id'], 0, 0, 0, 1, 0, 0, 0, 0)

                elif usuario['state_machine']['country'] == 1:
                    pais = user.message_text
                    if pais in paises:
                        # Insertamos el nuevo país
                        cluster.update_one({'id': usuario['id']}, {'$set': {'country': paises[pais]}})

                        # Respuesta de confirmación
                        if usuario['language'] == "es":
                            bot.send_message("*Ha elegido:* {}".format(pais), usuario['id'])
                        else:
                            bot.send_message("*You have selected:* {}".format(pais), usuario['id'])

                        # Respuesta automática
                        default_reply(usuario)
                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                    else:
                        if usuario['language'] == "es":
                            bot.send_message("Ha ocurrido un error, seleccione un país de la lista", usuario['id'])
                        else:
                            bot.send_message("An error has occurred, select a country from the list", usuario['id'])

                elif usuario['state_machine']['language'] == 1:
                    language = user.message_text
                    if language in languages:
                        # Insertamos el nuevo idioma
                        cluster.update_one({'id': usuario['id']}, {'$set': {'language': languages[language]}})

                        # Descarga del nuevo usuario
                        usuario = cluster.find_one({'id': usuario['id']})

                        # Respuesta de confirmación
                        if usuario['language'] == "es":
                            bot.send_message("*Ha elegido:* {}".format(language), usuario['id'])
                        else:
                            bot.send_message("*You have selected:* {}".format(language), usuario['id'])

                        # Respuesta automática
                        default_reply(usuario)
                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                    else:
                        if usuario['language'] == "es":
                            bot.send_message("Ha ocurrido un error, elija un idioma de la lista", usuario['id'])
                        else:
                            bot.send_message("An error has occurred, select a language from the list", usuario['id'])

                elif usuario['state_machine']['currency'] == 1:
                    divisa = user.message_text
                    if divisa in divisas:
                        # Actualizamos el rango de precios al cambio (en tiempo real) con la divisa
                        cluster.update_one(
                            {
                                'id': usuario['id']
                            }, {
                                '$set':
                                    {
                                        'range.max': round(
                                            c.convert(usuario['range']['max'], usuario['currency'], divisas[divisa]),
                                            2),
                                        'range.min': round(c.convert(usuario['range']['min'], usuario['currency'],
                                                                     divisas[divisa]), 2)
                                    }
                            }
                        )

                        # Insertamos la nueva divisa después de hacer el cambio de precios para tener la anterior divisa
                        cluster.update_one({'id': usuario['id']}, {'$set': {'currency': divisas[divisa]}})

                        # Respuesta de confirmación
                        if usuario['language'] == "es":
                            bot.send_message("*Ha elegido:* {}".format(divisa), usuario['id'])
                        else:
                            bot.send_message("*You have selected:* {}".format(divisa), usuario['id'])

                        # Respuesta automática
                        default_reply(usuario)

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)

                    else:
                        if usuario['language'] == "es":
                            bot.send_message("Ha ocurrido un error, elija una divisa de la lista", usuario['id'])
                        else:
                            bot.send_message("An error has occurred, select a currency from the list", usuario['id'])

                elif usuario['state_machine']['contact'] == 1:
                    try:
                        send_email(user.message_text)
                        if usuario['language'] == "es":
                            bot.send_message("Se ha enviado su mensaje", usuario['id'])
                        else:
                            bot.send_message("Your message has been sent", usuario['id'])

                        # Actualización del estado de la máquina de estados
                        state(usuario['id'], 0, 0, 0, 0, 0, 0, 0, 0)
                    except:
                        if usuario['language'] == "es":
                            bot.send_message("Ha habido un problema al enviar su mensaje, pruebe a no incluir "
                                             "caracteres especiales, si el problema persiste escriba el mensaje en "
                                             "inglés", usuario['id'])
                        else:
                            bot.send_message("An error has occurred, try to not include special characters",
                                             usuario['id'])

                else:  # A cualquier otra orden el bot solo hace la respuesta por defecto
                    default_reply(usuario)

            except:  # En caso de error se envía un correo al administrador para informarle de que algo ha fallado
                send_email("Ha ocurrido un error, es necesario realizar un mantenimiento")
                print("Error")
                pass
