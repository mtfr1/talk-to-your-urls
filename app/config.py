from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    PROJECT_NAME: str = "Talk to your URLs"
    VECTOR_COLLECTION_NAME: str = "url_indexer"


settings = Settings()
