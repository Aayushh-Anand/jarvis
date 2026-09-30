import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "J.A.R.V.I.S."
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


settings = Settings()