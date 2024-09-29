import wget

class URLListFileManager :

    def __init__(self, urlToDownloadFile: str, downloadListFilePath: str):
        self.urlToDownloadFile: str = urlToDownloadFile
        self.downloadListFilePath: str = downloadListFilePath

    def downloadURLListFile(self):
        wget.download(self.urlToDownloadFile, self.downloadListFilePath)