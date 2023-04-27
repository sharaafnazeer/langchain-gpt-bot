import pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENVIRONMENT"))


def create_index() -> None:
    pinecone.create_index(os.getenv("PINECONE_INDEX"), dimension=1536)  # default dinmension of openai is 1536


def delete_index() -> None:
    pinecone.delete_index(os.getenv("PINECONE_INDEX"))


def insert_vector(vectors) -> None:
    index = pinecone.Index(os.getenv("PINECONE_INDEX"))
    upsert_response = index.upsert(
        vectors=vectors,
        namespace="langchain-namespace"
    )
