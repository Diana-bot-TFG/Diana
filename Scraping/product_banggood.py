# Librerías
from bs4 import BeautifulSoup
import requests

# Módulos
from Python_server.initialization import c


# Clase
class Banggood_Product:

    def __init__(self, text, rango_min, rango_max, divisa, country):
        self.name = text
        self.country = country
        self.link = self.create_link()
        self.ID_producto = []
        self.Precio_producto = []
        self.Nombre_producto = []
        self.Link_producto = []
        self.Imagen_producto = []

        # Rango de precios dado por el usuario
        rango_precios = [rango_min, rango_max]

        # Inicialización de request
        headers = {"User-Agent": 'Mozilla\5.0'}
        page = requests.session().get(self.link, headers=headers)
        page_soup = BeautifulSoup(page.content, "html.parser")  # también vale lxml

        # Selección de los productos que son los que tienen la etiqueta shopslist
        items = page_soup.select(".shopslist ", namespaces=None)

        # Análisis de cada producto encontrado
        for i in range(len(items)):
            self.Nombre_producto.append(items[i].contents[1].contents[3].contents[1]["title"])
            self.ID_producto.append(items[i]["data-pid"])
            # Se usa find() para el precio para disminuir las interacciones para encontrar el producto y simplificar el código
            self.Precio_producto.append(
                round(c.convert(float(items[i].find("span", {"class": "price wh_cn"})['oriprice']), 'USD', divisa), 2))
            self.Link_producto.append(items[i].contents[1].contents[3].contents[1]["href"])
            self.Imagen_producto.append(items[i].contents[1].contents[1].contents[1].contents[1]["data-original"])

        # Selección de aquellos productos que están en el intervalo de precios
        if rango_precios:
            numero_productos = len(self.Precio_producto)
            for j in range(numero_productos):
                if float(rango_precios[0]) < float(self.Precio_producto[j]) < float(rango_precios[1]):
                    self.ID_producto.append(self.ID_producto[j])
                    self.Precio_producto.append(self.Precio_producto[j])
                    self.Nombre_producto.append(self.Nombre_producto[j])
                    self.Link_producto.append(self.Link_producto[j])
                    self.Imagen_producto.append(self.Imagen_producto[j])
                else:
                    pass
        for j in range(numero_productos):
            self.ID_producto.pop(0)
            self.Precio_producto.pop(0)
            self.Nombre_producto.pop(0)
            self.Link_producto.pop(0)
            self.Imagen_producto.pop(0)
        else:
            pass

        # Se imprimen por pantalla los productos para que los vea el desarrollador (opcional)
        print(self.Nombre_producto)
        print(self.Precio_producto)
        print(self.Link_producto)
        print(self.Imagen_producto)

    # Función
    def create_link(self):  # Crea el link de búsqueda en internet
        key_word = self.name.replace(" ", "%20")
        url = "https://www.banggood.com/search/{}.html".format(key_word)
        return url
