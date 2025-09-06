class Settings:
    client_id: str
    client_secret: str
    org_id: str

    ACCOUNTS_BASE_URL: str = "https://accounts.zoho.com"
    BOOKS_BASE_URL: str = "https://books.zoho.com"

    ENV_FILE: str = ".env"

    def __init__(self, client_id, client_secret, org_id=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.org_id = org_id
        self.ACCOUNTS_BASE_URL = "https://accounts.zoho.com/oauth/v2"
        self.BOOKS_BASE_URL = "https://www.zohoapis.com/books/v3"

    def save(self):
        with open(self.ENV_FILE, "w", encoding="utf-8") as f:
            if self.client_id:
                f.write(f'ZOHO_CLIENT_ID="{self.client_id}"\n')
            if self.client_secret:
                f.write(f'ZOHO_CLIENT_SECRET="{self.client_secret}"\n')
            if self.org_id:
                f.write(f'ZOHO_ORG_ID="{self.org_id}"\n')


settings = Settings(None, None)
