import os
import shutil
import YADS_4P.AllURLListComposer as AULC
import YADS_4P.AllURLListManager as AULM
import YADS_4P.common_functions as CF

class Exporter:


    def __init__(self , pathToBaseProjectFolder: str , pathToDatabase:str):
        self.PATH_TO_BASE_HOST_FILE = "/etc/hosts"
        self.PATH_TO_BACKUP_BASE_HOST_FILE = self.PATH_TO_BASE_HOST_FILE + "_old"
        self.PATH_TO_TEMP_BASE_HOST_FILE = self.PATH_TO_BASE_HOST_FILE + "_temp"
        self.CHECKMARK_TOKEN = "## YADS_CHECKMARK_TOKEN"
        self.pathToBaseProjectFolder = pathToBaseProjectFolder
        self.pathToDatabase = pathToDatabase

    def doHostFileExists(self):
        return os.path.isfile(self.PATH_TO_BASE_HOST_FILE)

    def doBackupHostFileExists(self):
        return os.path.isfile(self.PATH_TO_BACKUP_BASE_HOST_FILE)

    def doHostFileCheckmarkTokenExists(self):
        with open(self.PATH_TO_BASE_HOST_FILE , "r") as reader:
            for line in reader:
                if self.CHECKMARK_TOKEN in line:
                    return True
            return False

    def buildBackupHostFileIfPossible(self):
        # we are assuming that /etc/host already exist in a new installed linux based os, if it doesnot then it returns false.
        if (not self.doBackupHostFileExists() ) and self.doHostFileExists() and (not self.doHostFileCheckmarkTokenExists()) :
            shutil.copy(self.PATH_TO_BASE_HOST_FILE , self.PATH_TO_BACKUP_BASE_HOST_FILE)
            return True
        elif self.doBackupHostFileExists():
            return True
        else:
            return False


    def buildNewHostFile(self , downloadListFiles:bool = False ):

        if (self.buildBackupHostFileIfPossible()):
            shutil.copy(self.PATH_TO_BACKUP_BASE_HOST_FILE, self.PATH_TO_TEMP_BASE_HOST_FILE)
            self.addCheckmarkToken()
            self.addOtherDetails()
            if (downloadListFiles):
                self.addAllBlacklistedURLsAndReloadData()
            else :
                self.addAllBlacklistedURLs()

            # remove original
            CF.removeFileIfExists(self.PATH_TO_BASE_HOST_FILE)
            # rename temp to original
            shutil.copy(self.PATH_TO_TEMP_BASE_HOST_FILE, self.PATH_TO_BASE_HOST_FILE)

    def addCheckmarkToken(self):
        with open(self.PATH_TO_TEMP_BASE_HOST_FILE, "a") as writer:
            writer.write(self.CHECKMARK_TOKEN+"\n")

    def addOtherDetails(self):
        INSTRUCTIONS = """"""
        with open(self.PATH_TO_TEMP_BASE_HOST_FILE, "a") as writer:
            writer.write(INSTRUCTIONS+"\n")

    @staticmethod
    def addURLBlacklistRow(url:str)->str:
        return f"""0.0.0.0\t\t{url}\n"""


    def addAllBlacklistedURLs(self):
        with open(self.PATH_TO_TEMP_BASE_HOST_FILE, "a") as writer:
            aluc : AULC.ALLURLListComposer = AULC.ALLURLListComposer(self.pathToBaseProjectFolder , self.pathToDatabase)
            aluc.createNewComposerTable()
            aluc.feedDataIntoTable()
            for blocked_url in aluc.yieldAllUrls():
                writer.write(Exporter.addURLBlacklistRow(blocked_url))

    def addAllBlacklistedURLsAndReloadData(self):
        aulm : AULM.ALLURLListManager = AULM.ALLURLListManager(self.pathToBaseProjectFolder , self.pathToDatabase)
        aulm.reloadCompleteURLListOfAllURLs()
        self.addAllBlacklistedURLs()