# Módulos
from Python_server.initialization import cluster


# Función
def state(id, search, price_range, shops, tracking, country, language, currency, contact):  # Modifica la state machine
    cluster.update_one(
        {'id': id},
        {'$set':
            {
                'state_machine.search': search,
                'state_machine.price_range': price_range,
                'state_machine.shops': shops,
                'state_machine.tracking': tracking,
                'state_machine.country': country,
                'state_machine.language': language,
                'state_machine.currency': currency,
                'state_machine.contact': contact
            }
        }
    )
