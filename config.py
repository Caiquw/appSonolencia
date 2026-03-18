import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     "localhost",
    "database": "sonolencia",
    "user":     "postgres",
    "password": os.getenv("DB_PASSWORD")
}

SENDGRID_CONFIG = {
    "api_key":    os.getenv("SENDGRID_API_KEY"),
    "remetente":  "castro.caique@outlook.com",
    "supervisor": "sonolenciaappunaerp@outlook.com"
}