from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    mimoai_api_base_url: str
    mimoai_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore[call-arg]
