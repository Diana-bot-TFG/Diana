# Librerías
from bs4 import BeautifulSoup
import requests
import re

# Módulos
from Python_server.initialization import c


# Clase
class Ebay_Product:

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
        headers = {"User-Agent": 'Mozilla\5.0'}
        page = requests.get(self.link, headers=headers)
        page_soup = BeautifulSoup(page.content, "html.parser")  # también vale lxml

        # Selección de los productos que son los que tienen la etiqueta sresult lvresult clearfix li shic
        items = page_soup.select(".sresult.lvresult.clearfix.li.shic", namespaces=None)

        # Análisis de cada producto encontrado
        for i in range(len(items)):
            try:
                self.Nombre_producto.append(items[i].contents[1].contents[1].contents[1].contents[1]["alt"])
            except:
                self.Nombre_producto.append(items[i].contents[1].contents[1].contents[5].contents[1]["alt"])
            self.ID_producto.append(items[i]["listingid"])
            try:
                precio = str(items[i].contents[5].contents[1].contents[1].contents[0])
                number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                resul = float(number[0]) + (float(number[1]) / 100)
                self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
            except:
                try:
                    precio = str(items[i].contents[5].contents[1].contents[1].contents[1].contents[0])
                    number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                    resul = float(number[0]) + (float(number[1]) / 100)
                    self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                except:
                    try:
                        precio = str(items[i].contents[7].contents[1].contents[1].contents[0])
                        number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                        resul = float(number[0]) + (float(number[1]) / 100)
                        self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                    except:
                        try:
                            precio = str(items[i].contents[7].contents[1].contents[1].contents[1].contents[0])
                            number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                            resul = float(number[0]) + (float(number[1]) / 100)
                            self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                        except:
                            try:
                                precio = str(items[i].contents[9].contents[1].contents[1].contents[0])
                                number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                                resul = float(number[0]) + (float(number[1]) / 100)
                                self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                            except:
                                try:
                                    precio = str(items[i].contents[9].contents[1].contents[1].contents[1].contents[0])
                                    number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                                    resul = float(number[0]) + (float(number[1]) / 100)
                                    self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                                except:
                                    try:
                                        precio = str(items[i].contents[11].contents[1].contents[1].contents[0])
                                        number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                                        resul = float(number[0]) + (float(number[1]) / 100)
                                        self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
                                    except:
                                        precio = str(
                                            items[i].contents[11].contents[1].contents[1].contents[1].contents[0])
                                        number = re.findall(r"[-+]?\d*\.\d+|\d+", precio)
                                        resul = float(number[0]) + (float(number[1]) / 100)
                                        self.Precio_producto.append(round(c.convert(resul, 'USD', divisa), 2))
            try:
                self.Link_producto.append(items[i].contents[1].contents[1].contents[1]["href"])
            except:
                self.Link_producto.append(items[i].contents[1].contents[1].contents[5]["href"])
            if len(self.Link_producto[i]) > 300:    # recorta los links muy largos
                recorta1 = self.Link_producto[i].index("?")
                recorta2 = self.Link_producto[i].index("&")
                recorta3 = self.Link_producto[i][140:].index("&")
                self.Link_producto[i] = self.Link_producto[i][0:(recorta1+1)] + self.Link_producto[i][(recorta2+1):(140+recorta3)]
            try:
                self.Imagen_producto.append(items[i].contents[1].contents[1].contents[1].contents[1]["src"])
            except:
                self.Imagen_producto.append(items[i].contents[1].contents[1].contents[5].contents[1]["src"])

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
        j = 0
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
        url = "https://www.ebay.es/sch/i.html?_nkw={}".format(key_word)
        return url
