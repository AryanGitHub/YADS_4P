import os
import wget
import typing

import YADS_4P.URLListFileManager as ULFM
import YADS_4P.URLListFileParser  as ULFP
import YADS_4P.URLsListDatabaseManager as ULDM



class URLListManager:

    def __init__(self, url_id: int, urlToDownloadFile: str, pathToBaseFolder: str , pathToSQLDatabase : str):
        self.id: int = url_id
        self.pathToSQLDatabase = pathToSQLDatabase
        self.pathToBaseFolder: str = pathToBaseFolder #assuming this is already made
        self.urlToDownloadFile: str = urlToDownloadFile

        URLListManager.folder_setup(self.downloadListFolderPath)

    @property
    def downloadListFolderPath(self) -> str:
        return os.path.join(self.pathToBaseFolder, "list_"+str(self.id))
    @property
    def downloadListFilePath(self) -> str:
        return os.path.join(self.downloadListFolderPath, str(self.id) + ".txt")

    #@property
    #def pathToSQLDatabase(self) -> str:
    #    return os.path.join(self.pathToBaseFolder, self.NAME_OF_DATABASE_FILE)

    @property
    def getDatabaseTableName (self):
        return "Table_ID_" + str(self.id)

    @property
    def getOldDatabaseTableName (self):
        return "OldTable_ID_" + str(self.id)

    @staticmethod
    def folder_setup(pathToFolder: str):
        if not os.path.isdir(pathToFolder):
            os.mkdir(pathToFolder)



    def fetchURLListFile(self) -> None:
        self.fileManager : ULFM.URLListFileManager = ULFM.URLListFileManager(self.urlToDownloadFile , self.downloadListFilePath)
        self.fileManager.downloadURLListFile()

    def databaseTableSetUp(self) -> None:
        self.databaseTableManager = ULDM.URLsListDatabaseManager(self.id, self.pathToSQLDatabase , self.getDatabaseTableName , self.getOldDatabaseTableName)
        self.databaseTableManager.createNewOrReplaceTable()

    def parseFileToDatabaseTable(self) -> None:
        self.fileParser = ULFP.URLListFileParser(self.id,self.downloadListFilePath,self.pathToSQLDatabase , self.getDatabaseTableName)
        self.fileParser.insertAllURLsFromFileToDatabaseTable()


    def reloadCompleteURLList(self) -> None:
        """
            This function will completly 'reload or load' the list for 1st time...
            'reload or load' means 3 steps done one by one , one after another.

            1st step: fetch New List, and manage OLD list
                1.5th step: manage the database table, replace old one and build a new one...
            2nd step: parse the list, extract URLs from the list
            3rd step: insert all extracted URLs from the list to its own List
        """
        self.fetchURLListFile()
        self.databaseTableSetUp()
        self.parseFileToDatabaseTable()