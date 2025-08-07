class DatabaseConnectionFail(Exception):
    def __init__(self):
        self.message = '❌ A connection to the database could not be established.' 
        super().__init__(self.message)

class XboxApiWrapperError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)