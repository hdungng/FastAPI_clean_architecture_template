class AppException(Exception):
    StatusCode = 400

    def __init__(self, message: str):
        super().__init__(message)
        self.Message = message
