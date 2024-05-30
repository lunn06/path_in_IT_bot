from dotenv import load_dotenv
from pydantic import SecretStr, PositiveInt, DirectoryPath, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Config(BaseSettings):
    telegram_bot_token: SecretStr
    db_user: str
    db_name: str
    db_user_password: SecretStr
    db_host: IPvAnyAddress

    models_path: DirectoryPath
    initial_currency: PositiveInt
    interview_column_wight: PositiveInt

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config: Config = Config()  # type: ignore

if __name__ == "__main__":
    print(config.model_dump())
