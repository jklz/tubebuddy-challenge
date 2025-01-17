
class HttpRequestException(Exception):
    """
    Base exception for errors with http requests.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

class HttpNotFoundException(HttpRequestException):
    """
    Exception raised when an HTTP request fails with status code 404.
    """
    pass

class HttpInvalidRequestException(HttpRequestException):
    """
    Exception raised when an HTTP request fails with status code 4XX.
    """
    pass

class HttpServerException(HttpRequestException):
    """
    Exception raised when an HTTP request fails with status code 5XX.
    """
    pass

