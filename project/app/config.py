import logging
from functools import lru_cache
from pydantic import BaseSettings  # auto read from .env file
from pydantic import AnyUrl

log = logging.getLogger("uvicorn")

# when we create an instance of setting, environment and testing will have types of str and book
class Settings(BaseSettings):
    # BaseSettings will read from .env file => environment: str = "dev" is  environment: str = os.getenv("ENVIRONMENT", "dev").
    environment: str = "dev"  # dev, prod, test
    testing: bool = bool(0)  # whether we are testing
    database_url: AnyUrl = None

# since get_setting gets called for each request, we use lru_cache to cache the result of get_settings()
@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
