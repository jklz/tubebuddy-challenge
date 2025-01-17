import requests
from app.clients.http.exceptions import HttpNotFoundException, HttpServerException, HttpInvalidRequestException


async def http_get(url: str) -> requests.Response:
    """
    Send get request to http url with exceptions for any problem response status_codes
    """

    # get response from server
    response = requests.get(url)

    # check response status_code and throw exception for problem responses
    if response.status_code == 404:
        raise HttpNotFoundException(response.status_code, response.reason)
    elif response.status_code >= 500:
        raise HttpServerException(response.status_code, response.reason)
    elif response.status_code >= 400:
        raise HttpInvalidRequestException(response.status_code, response.reason)

    # return response
    return response

