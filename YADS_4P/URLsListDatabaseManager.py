import typing
import sqlite3
import YADS_4P.URLListOfListsManager as ULOLM
import YADS_4P.common_functions as CF


class URLsListDatabaseManager :

    def __init__(self , url_id : int , pathToSQLDatabase : str , databaseTableName :str , databaseOldTableName :str):
        self.url_id = url_id
        self.databaseTableName = databaseTableName
        self.databaseOldTableName = databaseOldTableName
        self.pathToSQLDatabase = pathToSQLDatabase

    def basic_table_setup(self) -> None:
        with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            query = f"""
                    CREATE TABLE {self.databaseTableName} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL
                    );
                """
            cursor.execute(query)

    def createNewOrReplaceTable(self) -> None:
        if self.URLTableAlreadyExists():
            if self.URLOldTableAlreadyExists():
                self.removeOldTable()
            self.moveToOldTable()
        self.basic_table_setup()


    def URLTableAlreadyExists(self) -> bool:
        return CF.tableAlreadyExists(self.pathToSQLDatabase , self.databaseTableName)

    def moveToOldTable(self) -> None:
        with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            query = f"ALTER TABLE {self.databaseTableName} RENAME TO {self.databaseOldTableName};"
            cursor.execute(query)
            sql_connection.commit()

    def URLOldTableAlreadyExists (self) -> bool :
        return CF.tableAlreadyExists(self.pathToSQLDatabase , self.databaseOldTableName)

    def removeOldTable (self) -> None:
        CF.removeTable(self.pathToSQLDatabase,self.databaseOldTableName)

    def addURLToTable(self, urlToAdd):
        if ULM.URLListOfListsManager.isValidURL(urlToAdd):
            with sqlite3.connect(self.pathToSQLDatabase) as sql_connection:
                cursor = sql_connection.cursor()
                cursor.execute(
                    f"""
                    INSERT INTO {self.databaseTableName} (url) VALUES ('{urlToAdd}'); 
                    """
                )
                sql_connection.commit()

