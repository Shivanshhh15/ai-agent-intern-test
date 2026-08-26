import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "text-embedding-3-small",
)

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "./chroma_db",
)

DEBUG = os.getenv(
    "DEBUG",
    "false",
).lower() == "true"