from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env_name: str
    base_url: str
    database_url: str

    class Config:
        env_file = ".env"

def get_settings():
    settings = Settings()
    return settings