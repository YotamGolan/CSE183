import mysql.connector
from mysql.connector.constants import ClientFlag
import json

class DBComm:
    
    cnxn = None
    cursor = None
    subtable = None

    def __init__(self, user, password, database):
        # Load the format of the submissions table
        file = open('data/subtable.json')
        subtable = json.load(file)
        
        # Connect to the database and create a cursor object
        config = self.__createConfig(user, password, database)
        self.cnxn = mysql.connector.connect(**config)
        self.cursor = self.cnxn.cursor()

    def __createConfig(self, user, password, database):
        # Load the format of the connection config
        file = open('data/config.json')
        config = json.load(file)
        
        # Add the necessary parameters
        config['client_flags'] = [ClientFlag.SSL]
        config['user'] = user
        config['password'] = password
        config['database'] = database
        
        return config

    def close(self):
        # Close the connection
        self.cnxn.close()
        del self.cnxn
    
    def insertPixel(self, user, x, y, r, g, b):
        if (cnxn):
            cursor.execute (
                "INSERT INTO {} ({}, {}, {}, {}, {}, {})".format(subtable['name'], subtable['user'], subtable['x'], subtable['y'], subtable['r'], subtable['g'], subtable['b']) + "VALUES ({}, {}, {}, {}, {}, {});".format(user, x, y, r, g, b)
            )
            cnxn.commit()
        else:
            print('[DBComm.insertPixel]: Tried to insert but connection was closed')

    def selectPixelsByUser(self, user):
        if (cnxn):
            cursor.execute(
                "SELECT * FROM {} WHERE {}='{}';".format(subtable['name'], subtable['user'], user)
            )

            out = cursor.fetchall()
            return out
        else:
            print('[DBComm.selectPixelsByUser]: Tried to select but connection was closed')

