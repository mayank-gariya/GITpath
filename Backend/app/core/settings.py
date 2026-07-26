from pydantic_settings import BaseSettings

class settings(BaseSettings):
    APP_NAME : str = 'GitPath'
    DEBUG : bool = True
    GITHUB_TOKEN : str

    REQUEST_TIMEOUT: int = 10
    
    class config:
        env_file = '.env'

setting = settings()