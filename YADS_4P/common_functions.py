
import sqlite3
import os

def tableAlreadyExists (databasePath :str , tableName :str ) -> bool:
    with sqlite3.connect(databasePath) as sql_connection:
        cursor = sql_connection.cursor()
        query = f"""
                SELECT name 
                FROM sqlite_master 
                WHERE type = 'table' 
                AND name = '{tableName}';
                """
        cursor.execute(query)
        dataFetched = cursor.fetchall()
    return len(dataFetched ) ==1 and dataFetched[0][0] == tableName

def removeTable (databasePath :str , tableName :str ) -> None:
    with sqlite3.connect(databasePath) as sql_connection:
        cursor = sql_connection.cursor()
        query = f"DROP TABLE IF EXISTS {tableName};"
        cursor.execute(query)
        sql_connection.commit()

def removeFileIfExists(filename : str) -> None:
    if (os.path.isfile(filename)):
        os.remove(filename)