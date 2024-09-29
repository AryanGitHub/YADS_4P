import YADS_4P.URLListOfListsManager as ULOLM
import YADS_4P.URLListManager as ULM
class ALLURLListManager:

    def __init__(self , pathToBaseFolder:str ,pathToDatabase :str ):
        self.pathToBaseFolder = pathToBaseFolder
        self.pathToDatabase = pathToDatabase
        self.urlListManagers : [URLListManager] = []
        self.setAllURLListsManagers()

    def setAllURLListsManagers(self):
        ulolm : ULOLM.URLListOfListsManager = ULOLM.URLListOfListsManager(self.pathToDatabase)
        for row_id , row_url in ulolm.yieldAllURLsWithID():
            self.urlListManagers.append( ULM.URLListManager(row_id , row_url ,self.pathToBaseFolder , self.pathToDatabase) )

    def reloadCompleteURLListOfAllURLs (self):
        for url_manager in self.urlListManagers:
            url_manager.reloadCompleteURLList()
