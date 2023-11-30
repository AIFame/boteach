import os
from os import environ
from typing import Final

from dotenv import load_dotenv

load_dotenv()

APP_NAME: Final = "boteach"

PRODUCTION: Final[str] = "prod"
DEVELOPMENT: Final[str] = "dev"
TESTING: Final[str] = "test"
MODE: Final[str] = os.getenv("mode", PRODUCTION)

PINECONE_API_KEY: Final[str] = environ["PINECONE_API_KEY"].strip()
PINECONE_API_ENV: Final[str] = environ["PINECONE_API_ENV"].strip()
INDEX_NAME: Final[str] = environ.get("PINECONE_INDEX_NAME", APP_NAME)

OPENAI_API_KEY: Final[str] = environ["OPENAI_API_KEY"].strip()
OPENAI_ORGANIZATION_ID: Final[str] = environ.get(
    "OPENAI_ORGANIZATION_ID",
    "",
).strip()
OPENAI_ASSISTANT_ID: Final = environ.get(
    "OPENAI_ASSISTANT_ID", "asst_frmjonf13TDEk4WIzDWwZNVN"
).strip()
# TODO: create assistants for every session
OPENAI_EMBEDDINGS_LLM: Final[str] = os.getenv(
    "OPENAI_EMBEDDINGS_LLM",
    "text-embedding-ada-002",
).strip()
OPENAI_CHAT_MODEL: Final[str] = os.getenv(
    "OPENAI_CHAT_MODEL",
    "gpt-3.5-turbo",
).strip()

VIDEO_PATH: Final = os.path.join("data", "Neurons and the brain.mp4")
VIDEO_TRANSCRIPT_PATH: Final = os.path.join("data", "Neurons and the brain.txt")
