import mysql.connector
from mysql.connector.constants import ClientFlag

# parameters for the database connection
config = {
    'user': 'Mitchell',
    'password': 'Mitchellpass123',
    'host': '146.148.46.129',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem',
    'database': 'canvasDB'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)
# create a cursor object
cursor = cnxn.cursor()

cursor.execute(
    "DESCRIBE Submissions;"
)

out = cursor.fetchall()
for row in out:
    print(row)


#cursor.execute(
#    "DESCRIBE Submissions;"
#)

#out = cursor.fetchall()
#for row in out:
#    print(row)
# close the connection
cnxn.close()
