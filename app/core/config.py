from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CHROMA_PATH: str = "./chroma_db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() # type: ignore