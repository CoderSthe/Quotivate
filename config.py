import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.environ.get("SMTP_LOGIN")
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")

if not all([EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT]):
    raise EnvironmentError("Missing required environment variables. Please set SMTP_LOGIN, SMTP_PASSWORD, SMTP_SERVER, and SMTP_PORT.")