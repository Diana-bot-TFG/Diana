# Módulos
from Scraping.product_ebay import Ebay_Product
from Scraping.product_banggood import Banggood_Product
from Scraping.product_gearbest import Gearbest_Product
from Python_server.initialization import bot
from Dictionaries.dictionaries import divisas_simbolo


# Función
def check(id, Product, Country, Currency, Min, Max, Select_Ebay, Select_Gearbest, Select_Banggood, usuario):
    # Únicamente se comprueban las webs seleccionadas por el usuario
    if Select_Ebay:
        ebay = Ebay_Product(Product, Min, Max, Currency, Country)
    if Select_Gearbest:
        gearbest = Gearbest_Product(Product, Min, Max, Currency, Country)
    if Select_Banggood:
        banggood = Banggood_Product(Product, Min, Max, Currency, Country)
    # Se comprueba si el producto de menor precio encontrado, cumple los márgenes de precio establecido y se envía
    if Select_Ebay:
        try:
            min_ebay = ebay.Precio_producto.index(min(ebay.Precio_producto))
            if usuario['language'] == 'es':
                bot.send_message(
                    "[{}]\n\nHe encontrado su producto *{}* en *Ebay*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        ebay.Imagen_producto[min_ebay], Product, ebay.Nombre_producto[min_ebay],
                        ebay.Precio_producto[min_ebay], divisas_simbolo[Currency],
                        ebay.Link_producto[min_ebay]), id)
            else:
                bot.send_message(
                    "[{}]\n\nI have found your product *{}* on *Ebay*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        ebay.Imagen_producto[min_ebay], Product, ebay.Nombre_producto[min_ebay],
                        ebay.Precio_producto[min_ebay], divisas_simbolo[Currency],
                        ebay.Link_producto[min_ebay]), id)
        except:  # En caso de no haber un producto en el rango deseado, no se envía nada
            pass
    if Select_Gearbest:
        try:
            min_gearbest = gearbest.Precio_producto.index(min(gearbest.Precio_producto))
            if usuario['language'] == 'es':
                bot.send_message(
                    "[{}]\n\nHe encontrado su producto *{}* en *Gearbest*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        gearbest.Imagen_producto[min_gearbest], Product, gearbest.Nombre_producto[min_gearbest],
                        gearbest.Precio_producto[min_gearbest], divisas_simbolo[usuario['currency']],
                        gearbest.Link_producto[min_gearbest]), id)
            else:
                bot.send_message(
                    "[{}]\n\nI have found your product *{}* on *Gearbest*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        gearbest.Imagen_producto[min_gearbest], Product, gearbest.Nombre_producto[min_gearbest],
                        gearbest.Precio_producto[min_gearbest], divisas_simbolo[usuario['currency']],
                        gearbest.Link_producto[min_gearbest]), id)
        except:
            pass
    if Select_Banggood:
        try:
            min_banggood = banggood.Precio_producto.index(min(banggood.Precio_producto))
            if usuario['language'] == 'es':
                bot.send_message(
                    "[{}]\n\nHe encontrado su producto *{}* en *Banggood* on *Banggood*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        banggood.Imagen_producto[min_banggood], Product, banggood.Nombre_producto[min_banggood],
                        banggood.Precio_producto[min_banggood], divisas_simbolo[usuario['currency']],
                        banggood.Link_producto[min_banggood]), id)
            else:
                bot.send_message(
                    "[{}]\n\nI have found your product *{}* on *Banggood*:\n\n{}\n\n*Precio:*\n{} {}\n\n*Link:*\n[{}]".format(
                        banggood.Imagen_producto[min_banggood], Product, banggood.Nombre_producto[min_banggood],
                        banggood.Precio_producto[min_banggood], divisas_simbolo[usuario['currency']],
                        banggood.Link_producto[min_banggood]), id)
        except:
            pass
