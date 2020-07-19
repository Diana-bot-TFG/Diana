# Librerías
import smtplib
import configparser as cfg
from email.mime.text import MIMEText


# Función
def send_email(msg):
    # Creamos un servidor
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Sacamos la contraseña de un archivo config.cfg
    parser = cfg.ConfigParser()
    parser.read('config.cfg')
    password = parser.get('email', 'email_diana')

    # Iniciamos sesión
    server.login('dianabot2020@gmail.com', password)

    # Hacemos que se puedan enviar caracteres no-ASCII
    msg_tosend = MIMEText(msg, 'plain', 'latin-1').as_string()

    # Enviamos el mensaje
    server.sendmail('dianabot2020@gmail.com', 'dianabot2020@gmail.com', msg_tosend)

    # Cerramos el servidor
    server.quit()
