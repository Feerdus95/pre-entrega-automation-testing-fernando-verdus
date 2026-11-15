import logging

import requests

logger = logging.getLogger("saucedemo")

API_BASE_URL = "https://jsonplaceholder.typicode.com"
API_TIMEOUT = 10


class ApiClient:
    """Thin wrapper over requests: returns the raw Response, never raises on HTTP errors.

    Connection errors and timeouts raise ConnectionError naming the service and request.
    """

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.request(method, url, timeout=API_TIMEOUT, **kwargs)
        except (requests.ConnectionError, requests.Timeout) as exc:
            # Connectivity problems fail with a message naming the external service
            logger.error("API %s %s -> unavailable: %s", method, url, type(exc).__name__)
            raise ConnectionError(
                f"External API unavailable: {method} {url} ({type(exc).__name__}: {exc})"
            ) from exc
        # response.url includes the encoded query string sent in params
        logger.info("API %s %s -> %s", method, response.url, response.status_code)
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self.session.close()
