

class bootstrap:

    def __init__(self , pathToBaseFolder):
        self.pathToBaseFolder = pathToBaseFolder
        bootstrap.folder_setup(self.pathToBaseFolder)


    @staticmethod
    def folder_setup(pathToFolder):
        if not os.path.isdir(pathToDownloadFolder):
            os.mkdir(pathToDownloadFolder)