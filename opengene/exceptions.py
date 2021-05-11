from PySide2.QtCore import QCoreApplication


class UnrecognizedFileFormatError(Exception):
    """Exception raised when opened file is not recognized

    Attributes:
        file -- file name
    """
    def __init__(self, file, message=QCoreApplication.translate("UnrecognizedFileFormat", "The file is not in a recognized format")):
        self.file = file
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"File :\"{self.file}\" {self.message}"
