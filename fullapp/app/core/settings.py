import streamlit as st
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "GitPath"
    DEBUG: bool = True

    # Pull from st.secrets if env variable is not present
    GITHUB_TOKEN: str = st.secrets.get("GITHUB_TOKEN", "")

    REQUEST_TIMEOUT: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
