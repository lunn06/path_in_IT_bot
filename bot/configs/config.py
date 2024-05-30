from functools import lru_cache

from environs import Env
from pydantic import SecretStr, PositiveInt, DirectoryPath, IPvAnyAddress
from pydantic_settings import BaseSettings

env = Env()
env.read_env()


class Config(BaseSettings):
    telegram_bot_token: SecretStr
    db_user: str
    db_name: str
    db_user_password: SecretStr
    db_host: IPvAnyAddress

    models_path: DirectoryPath
    initial_currency: PositiveInt
    interview_column_wight: PositiveInt

    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


@lru_cache(maxsize=1)
def parse_config():
    return Config()


if __name__ == "__main__":
    config = parse_config()
    config2 = parse_config()

    assert parse_config() is parse_config() is parse_config() is parse_config()
    # print(parse_config().model_dump())
