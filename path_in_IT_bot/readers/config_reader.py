from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Config(BaseSettings):
    telegram_bot_token: SecretStr
    db_user: str
    db_name: str
    db_user_password: SecretStr
    db_host: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config: Config = Config()  # type: ignore

if __name__ == "__main__":
    print(config.model_dump())
