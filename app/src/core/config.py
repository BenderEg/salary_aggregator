from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseSettings):
    host: str
    port: int

    @property
    def connection(self):
        return f"mongodb://{self.host}:{self.port}/?uuidRepresentation=standard"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )
    mongo: MongoSettings
    token: str

settings = Settings()