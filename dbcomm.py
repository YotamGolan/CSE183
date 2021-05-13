import mysql.connector
from mysql.connector.constants import ClientFlag
import json

class DBComm:
    
    cnxn = None
    cursor = None

    def __init__(self, user, password, database):
        config = self.__createConfig(user, password, database)
        self.cnxn = mysql.connector.connect(**config)
        self.cursor = self.cnxn.cursor()

    def __createConfig(self, user, password, database):
        file = open('data/config.json')

        config = json.load(file)
        config['client_flags'] = [ClientFlag.SSL]
        config['user'] = user
        config['password'] = password
        config['database'] = database
        
        return config

    def close(self):
        self.cnxn.close()
        del self.cnxn
    
    def insertPixel(self, user, x, y, r, g, b):
        if (cnxn):
            cursor.execute (
                "INSERT INTO Submissions (userID, xCoord, yCoord, rValue, gValue, bValue) VALUES ({}, {}, {}, {}, {}, {});".format(user, x, y, r, g, b)
            )
        else:
            print('[DBComm.insertPixel]: Tried to insert but connection was closed')
