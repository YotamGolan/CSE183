import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'Mitchell',
    'password': 'Mitchellpass123',
    'host': '146.148.46.129',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)
