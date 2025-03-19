import uvicorn
from pydantic_settings import BaseSettings


class UvicornSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 6000
    RELOAD: bool = False


uvicorn_settings = UvicornSettings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=uvicorn_settings.HOST,
        port=uvicorn_settings.PORT,
        reload=uvicorn_settings.RELOAD,
    )
