import re
import sqlite3
import typing
class URLListFileParser:

    def __init__(self,url_id , URLListFilePath:str,URLListDatabasePath:str , URLListTableName ):
        self.url_id = url_id
        self.URLListFilePath = URLListFilePath
        self.URLListDatabasePath = URLListDatabasePath
        self.URLListTableName = URLListTableName

    def yieldNextURL(self)->str:
        """yields next URL from the file, doing this lazily using generator, to handle large files"""
        with open(self.URLListFilePath , "r") as fileReader:
            for line in fileReader:
                url_extracted = URLListFileParser.extractURLFromLine(line)
                if url_extracted is not None:
                    yield url_extracted
    @staticmethod
    def additionalOperationsOnURL (url:str)->str:
        """based on observation, some mannual operations were done.
            this function is to be applied after extraction of URL is done."""

        """check 1: if URL starts with 0.0.0.0 then remove it. like 0.0.0.0advanced-options.ml should be just advanced-options.ml"""
        if url.startswith("0.0.0.0"):
            url = url[len("0.0.0.0"):]

        """add other checks here like check 2 and so on.... """

        return url
    @staticmethod
    def extractURLFromLine (line :str , returnList = None) -> list[str]:
        if returnList == None:
            returnList = []

        line = line.strip()
        if line.startswith("#") or line.startswith("//") or line.startswith("!"):
            return None
        parts = line.split(" ")
        if len (parts) > 1:
            for x in parts:
                URLListFileParser.extractURLFromLine(x,returnList)
            if (len(returnList)>0):
                return returnList
            else:
                return None
        else :
            part = parts[0]
            # taken from https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
            # and https://regexr.com/3e6m0

            url_pattern = re.compile(r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
            urls = url_pattern.finditer(part)

            newReturnList = []
            for match in urls:
                url = match.group()
                url = URLListFileParser.additionalOperationsOnURL(url)
                newReturnList.append(url)

            if len(newReturnList)>0:
                returnList.extend(newReturnList)
                return returnList
            else:
                return None

    def insertAllURLsFromFileToDatabaseTable(self):
        with sqlite3.connect(self.URLListDatabasePath) as sql_connect :
            cursor = sql_connect.cursor()
            for URLsToInsert in self.yieldNextURL():
                for singleURL in URLsToInsert:
                    query = f"""
                            INSERT INTO {self.URLListTableName} (url) VALUES ('{singleURL}'); 
                            """
                    sql_connect.execute(query)
            sql_connect.commit()