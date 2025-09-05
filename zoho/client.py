import requests

from .settings import settings

class Client:
    """Base Zoho Books API client with authentication and common operations"""

    def __init__(self):
        # Use provided credentials or load from settings
        # Initialize access_token as None, will be set when needed
        self.access_token = None
        self.headers = {}
        self.errors = {}

    def _ensure_access_token(self):
        """Ensure access token is available"""
        if not self.access_token:
            self.access_token = self._get_access_token()
            self.headers = {
                "Authorization": f"Zoho-oauthtoken {self.access_token}",
                "content-type": "application/json",
            }

    def _get_access_token(self):
        """Get access token using refresh token"""
        url = f"{settings.ACCOUNTS_BASE_URL}/token"
        params = {
            "refresh_token": settings.refresh_token,
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "grant_type": "refresh_token",
        }
        response = requests.post(url, params=params)
        return response.json()["access_token"]

    def _make_request(self, method, endpoint, params=None, json_data=None):
        """Make API request with error handling"""
        self._ensure_access_token()
        url = f"{settings.BOOKS_BASE_URL}/{endpoint}"
        params = params or {}
        params["organization_id"] = settings.org_id

        response = requests.request(method, url, params=params, json=json_data, headers=self.headers)
        response_json = response.json()

        if response_json.get("code", 0) != 0:
            self._handle_error(response_json)

        return response_json

    def _handle_error(self, response_json):
        """Handle API errors"""
        error_code = response_json.get("code")
        error_message = response_json.get("message", "Unknown error")

        if error_code not in self.errors:
            self.errors[error_code] = {
                "error": error_message,
                "items": [],
            }

        # Add context to error tracking
        if "name" in response_json:
            self.errors[error_code]["items"].append(response_json["name"])

        print(f"Error {error_code}: {error_message}")

    def get(self, endpoint, params=None):
        """Make GET request"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint, json_data, params=None):
        """Make POST request"""
        return self._make_request("POST", endpoint, params=params, json_data=json_data)

    def put(self, endpoint, json_data, params=None):
        """Make PUT request"""
        return self._make_request("PUT", endpoint, params=params, json_data=json_data)

    def delete(self, endpoint, params=None):
        """Make DELETE request"""
        return self._make_request("DELETE", endpoint, params=params)

client = Client()
