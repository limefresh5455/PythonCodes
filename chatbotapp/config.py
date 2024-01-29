from os import environ

DATABASE_URL = environ.get("DATABASE_URL")
COLLECTION_NAME = environ.get("COLLETION_NAME")
OPENAI_API_KEY = environ.get("OPENAI_API_KEY")
