from pydantic_settings import BaseSettings

class settings(BaseSettings):
    APP_NAME : str = 'GitPath'
    DEBUG : bool = True
    GITHUB_TOKEN : str

    class config:
        env_file = '.env'

setting = settings()