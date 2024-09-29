import YADS_4P.common_functions as CF
import YADS_4P.AllURLListManager as AULM
import YADS_4P.URLListManager as ULM
import sqlite3

class ALLURLListComposer:

    def __init__(self,pathToBaseFolder:str ,pathToDatabase :str ):
        self.pathToBaseFolder = pathToBaseFolder
        self.pathToDatabase = pathToDatabase
        self.DATABASE_TABLE_NAME = "Composer"


    def doComposerTableExists(self) -> bool:
        return CF.tableAlreadyExists(self.pathToDatabase , self.DATABASE_TABLE_NAME)

    def removeComposerTable(self) -> None:
        CF.removeTable(self.pathToDatabase , self.DATABASE_TABLE_NAME)

    def basic_table_setup(self) -> None:
        with sqlite3.connect(self.pathToDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            query = f"""
                    CREATE TABLE {self.DATABASE_TABLE_NAME} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT NOT NULL
                    );
                """
            cursor.execute(query)


    def createNewComposerTable(self) -> None:
        if self.doComposerTableExists():
            self.removeComposerTable()
        self.basic_table_setup()

    def buildQuery(self) -> str:

        """the query we are building is like this

            INSERT OR IGNORE INTO unique_urls_table (URL)
            SELECT URLs FROM table1
            UNION
            SELECT URLs FROM table2
            UNION
            SELECT URLs FROM table3;

        """
        query = f"INSERT OR IGNORE INTO {self.DATABASE_TABLE_NAME} (URL)\n"

        alum : AULM.ALLURLListManager = AULM.ALLURLListManager(self.pathToBaseFolder , self.pathToDatabase)
        firstTable : bool = True
        for ulm in alum.urlListManagers :
            addedQuery = ""
            if not firstTable:
                addedQuery += " UNION\n"
            if firstTable:
                firstTable = False
            addedQuery += f"SELECT url FROM {ulm.getDatabaseTableName}\n"
            query+=addedQuery
        query+=";"
        return query

    def feedDataIntoTable (self):
        with sqlite3.connect(self.pathToDatabase) as sql_connection:
            cursor = sql_connection.cursor()
            query = self.buildQuery()
            cursor.execute(query)
            sql_connection.commit()

    def yieldAllUrls(self):
        """Returns a tuple of all added URLs"""
        with sqlite3.connect(self.pathToDatabase) as sql_connection:
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

