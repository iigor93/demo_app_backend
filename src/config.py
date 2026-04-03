from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    s3_access_key: str
    s3_secret_key: str
    s3_host: str
    s3_port: int
    s3_bucket: str
    s3_secure: bool
    s3_type: str
    public_base_url: str | None = None

    admin_username: str
    admin_password: str
    admin_secret_key: str

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def s3_endpoint(self) -> str:
        protocol = "https" if self.s3_secure else "http"
        return f"{protocol}://{self.s3_host}:{self.s3_port}"

    @computed_field
    @property
    def public_s3_base(self) -> str:
        if self.public_base_url:
            return self.public_base_url
        return self.s3_endpoint


settings = Settings()
