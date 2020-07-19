# Módulos
from Python_server.initialization import cluster
from Functions.check import check


# Función
def tracking():
    # Extraemos todos los usuarios que tengan productos
    usuarios = cluster.find({"products.name_product": {"$ne": None}})

    # Vamos usuario a usuario y enviamos un mensaje si el producto deseado está al precio establecido
    for usuario in usuarios:
        for i in range(len(usuario['products'])):
            check(usuario['id'], usuario['products'][i]['name_product'], usuario['country'], usuario['currency'],
                  usuario['products'][i]['price_product_min'], usuario['products'][i]['price_product_max'],
                  usuario['shops']['Ebay'], usuario['shops']['Gearbest'], usuario['shops']['Banggood'], usuario)
