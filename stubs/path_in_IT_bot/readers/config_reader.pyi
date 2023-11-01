from _typeshed import Incomplete
from pydantic import SecretStr as SecretStr
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    telegram_bot_token: SecretStr
    db_user: str
    db_name: str
    db_user_password: SecretStr
    db_host: str
    model_config: Incomplete

config: Config
