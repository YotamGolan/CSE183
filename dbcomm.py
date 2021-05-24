import mysql.connector
from mysql.connector.constants import ClientFlag
import json
import os

APP_FOLDER = os.path.dirname(__file__)
class DBComm:
    

    def __init__(self, user, password, database):
        self.connect(user, password, database)

    def __createConfig(self, user, password, database):
        # Load the format of the connection config
        file = os.path.join(APP_FOLDER, "data", "config.json")
        config = json.load(open(file))
        
        # Add the necessary parameters
        config['client_flags'] = [ClientFlag.SSL]
        config['user'] = user
        config['password'] = password
        config['database'] = database
        
        return config
    
    def connect(self, user, password, database):
        # Load the format of the submissions table
        file = os.path.join(APP_FOLDER, "data", "subtable.json")
        self.subtable = json.load(open(file))
        
        # Load the format for the users table
        file = os.path.join(APP_FOLDER, "data", "userstable.json")
        self.userstable = json.load(open(file))

        # Connect to the database and create a cursor object
        config = self.__createConfig(user, password, database)
        print(config)
        self.cnxn = mysql.connector.connect(**config)
        self.cursor = self.cnxn.cursor()

    def close(self):
        # Close the connection
        self.cnxn.close()
        del self.cnxn
   

    def insertUser(self, userID, firstName, lastName, pixelCount):
        if (self.cnxn):
            self.cursor.execute (
                f"INSERT INTO {self.userstable['name']} ({self.userstable['user']}, {self.userstable['first']}, {self.userstable['last']}, {self.userstable['pixels']}) VALUES ({userID}, '{firstName}', '{lastName}', {pixelCount});"
            )
            self.cnxn.commit()
        else:
            print('[DBComm.insertUser]: Tried to insert but connection was closed')

 

    def insertPixel(self, user, x, y, r, g, b):
        if (self.cnxn):
            self.cursor.execute (
                f"INSERT INTO {self.subtable['name']} ({self.subtable['user']}, {self.subtable['x']}, {self.subtable['y']}, {self.subtable['r']}, {self.subtable['g']}, {self.subtable['b']}) VALUES ({user}, {x}, {y}, {r}, {g}, {b});"
            )
            self.cnxn.commit()
        else:
            print('[DBComm.insertPixel]: Tried to insert but connection was closed')

    def selectPixelsByUser(self, user):
        if (self.cnxn):
            self.cursor.execute(
                f"SELECT * FROM {self.subtable['name']} WHERE {self.subtable['user']}={user};"
            )

            out = self.cursor.fetchall()
            return out
        else:
            print('[DBComm.selectPixelsByUser]: Tried to select but connection was closed')


    def selectUserData(self, user):
        if (self.cnxn):
            self.cursor.execute(
                f"SELECT * FROM {self.userstable['name']} WHERE {self.userstable['user']}={user};"
            )

            out = self.cursor.fetchall()
            return out
        else:
            print('[DBComm.selectUserData]: Tried to select but connection was closed')

    def selectAllUserData(self):
        if (self.cnxn):
            self.cursor.execute(
                f"SELECT * FROM {self.userstable['name']};"
            )

            out = self.cursor.fetchall()
            return out
        else:
            print('[DBComm.selectAllUserData]: Tried to select but connection was closed')

    def selectPixelMatrix(self, index):
        out = None
        if (self.cnxn):
            try:
                self.cursor.execute(
                    f"SELECT * FROM {self.subtable['name']} WHERE {self.subtable['id']} >= {index}"
                )
                out = self.cursor.fetchall()
            except:
               print("[DBComm.selectPixelMatrix]: Could not select with those parameters")
        else:
            print('[DBComm.selectPixelMatrix]: Tried to select but connection was closed')
            
        return out

