import re  # for regex
import os
import sqlite3

class URLListOfListsManager:
    def __init__(self, pathToSQLDatabase):

        self.cursor = None
        self.sql_connection = None
        self.DATABASE_TABLE_NAME = "block_list_of_lists"
        self.pathToSQLDatabase = pathToSQLDatabase

        self.database_table_setup()


    def database_table_setup(self):
        """setup the database table"""
        with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            query = f"""
                    CREATE TABLE IF NOT EXISTS {self.DATABASE_TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL
                    );
                    """
            cursor.execute(query)

    def addURL(self, urlToAdd):
        if URLListOfListsManager.isValidURL(urlToAdd):
            with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
                cursor = sql_connection.cursor()
                cursor.execute(

                    f"""
                    INSERT INTO {self.DATABASE_TABLE_NAME} (url) VALUES ('{urlToAdd}'); 
                    """
                )
                sql_connection.commit()

    @staticmethod
    def isValidURL(url:str):
        # this regex is taken from : https://www.freecodecamp.org/news/how-to-write-a-regular-expression-for-a-url/
        p = re.compile(
            """(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?""")
        if (d:= p.match(url)) is not None:
            return True
        else:
            return False

    def yieldAllURLsWithID(self):
        """Returns a tuple of all added URLs"""
        with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
            cursor = sql_connection.cursor()

            cursor.execute(
                f"""
                SELECT id,url FROM {self.DATABASE_TABLE_NAME};
                """
            )

            while True:
                data = cursor.fetchone()
                if data != None:
                    yield data
                else:
                    break


    def yieldAllURLs(self):
        """Returns a tuple of all added URLs"""
        with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            cursor.execute(
                f"""
                SELECT url FROM {self.DATABASE_TABLE_NAME};
                """
            )
            while True:
                data = cursor.fetchone()
                if data != None:
                    yield data[0]
                else:
                    break


    def getAllURLsWithID(self):
        """Returns a tuple of all added URLs"""
        return list(self.yieldAllURLsWithID())

    def getAllURLs(self):
        """Returns a tuple of all added URLs"""
        return list(self.yieldAllURLs())
