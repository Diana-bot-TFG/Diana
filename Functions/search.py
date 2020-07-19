# Módulos
from Scraping.product_ebay import Ebay_Product
from Scraping.product_banggood import Banggood_Product
from Scraping.product_gearbest import Gearbest_Product
from Python_server.initialization import bot
from Dictionaries.dictionaries import divisas_simbolo


# Función
def search(item, Select_Ebay, Select_Gearbest, Select_Banggood, Link_Activos, usuario):
    # Fase de búsqueda en las webs seleccionadas por el usuario
    if Select_Ebay:
        ebay = Ebay_Product(
            item, usuario['range']['min'], usuario['range']['max'], usuario['currency'], usuario['country'])

    if Select_Gearbest:
        gearbest = Gearbest_Product(
            item, usuario['range']['min'], usuario['range']['max'], usuario['currency'], usuario['country'])

    if Select_Banggood:
        banggood = Banggood_Product(
            item, usuario['range']['min'], usuario['range']['max'], usuario['currency'], usuario['country'])

    # Fase de envío del link si así lo pide el usuario
    if Link_Activos:
        if Select_Ebay:
            bot.send_message("*Ebay*\n[{}]".format(ebay.link), usuario['id'])

        if Select_Gearbest:
            bot.send_message("*Gearbest*\n[{}]".format(gearbest.link), usuario['id'])

        if Select_Banggood:
            bot.send_message("*Banggood*\n[{}]".format(banggood.link), usuario['id'])

    # Fase de envío de la mejor opción, si no encuentra nada que cumpla los límites, envía un mensaje predeterminado
    if Select_Ebay:
        try:
            min_ebay = ebay.Precio_producto.index(min(ebay.Precio_producto))
            bot.send_message("[{}]\n\n*Ebay:*\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                ebay.Imagen_producto[min_ebay], ebay.Nombre_producto[min_ebay],
                ebay.Precio_producto[min_ebay], divisas_simbolo[usuario['currency']],
                ebay.Link_producto[min_ebay]), usuario['id'])

        except:
            if usuario['language'] == 'es':
                bot.send_message("*Ebay:*\nNo he encontrado nada en Ebay", usuario['id'])
            else:
                bot.send_message("*Ebay:*\nI have not found anything on Ebay", usuario['id'])

    if Select_Gearbest:
        try:
            min_gearbest = gearbest.Precio_producto.index(min(gearbest.Precio_producto))
            bot.send_message("[{}]\n\n*Gearbest:*\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                gearbest.Imagen_producto[min_gearbest], gearbest.Nombre_producto[min_gearbest],
                gearbest.Precio_producto[min_gearbest], divisas_simbolo[usuario['currency']],
                gearbest.Link_producto[min_gearbest]), usuario['id'])

        except:
            if usuario['language'] == 'es':
                bot.send_message("*Gearbest:*\nNo he encontrado nada en Gearbest", usuario['id'])
            else:
                bot.send_message("*Gearbest:*\nI have not found anything on Gearbest", usuario['id'])

    if Select_Banggood:
        try:
            min_banggood = banggood.Precio_producto.index(min(banggood.Precio_producto))
            bot.send_message("[{}]\n\n*Banggood:*\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                banggood.Imagen_producto[min_banggood], banggood.Nombre_producto[min_banggood],
                banggood.Precio_producto[min_banggood], divisas_simbolo[usuario['currency']],
                banggood.Link_producto[min_banggood]), usuario['id'])

        except:
            if usuario['language'] == 'es':
                bot.send_message("*Banggood:*\nNo he encontrado nada en Banggood", usuario['id'])
            else:
                bot.send_message("*Banggood:*\nI have not found anything on Banggood", usuario['id'])
