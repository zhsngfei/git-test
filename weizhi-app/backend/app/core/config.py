from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PLACEHOLDER_VALUES = {
    "https://example.supabase.co",
    "replace-with-service-role-key",
    "replace-with-supabase-jwt-secret-at-least-32-characters",
    "https://api.example.com",
    "replace-with-mimoai-key",
}


class Settings(BaseSettings):
    app_env: str = "local"
    frontend_origin: str = "http://localhost:3000"
    supabase_url: str = "https://example.supabase.co"
    supabase_service_role_key: str = "replace-with-service-role-key"
    supabase_jwt_secret: str = "replace-with-supabase-jwt-secret-at-least-32-characters"
    mimoai_api_base_url: str = "https://api.example.com"
    mimoai_api_key: str = "replace-with-mimoai-key"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @model_validator(mode="after")
    def reject_production_placeholders(self) -> "Settings":
        if self.app_env == "local":
            return self

        supabase_values = {
            self.supabase_url,
            self.supabase_service_role_key,
            self.supabase_jwt_secret,
        }
        if supabase_values & PLACEHOLDER_VALUES:
            raise ValueError("Non-local settings must not use Supabase placeholder values")

        production_values = {
            self.mimoai_api_base_url,
            self.mimoai_api_key,
        }
        if self.app_env == "production" and production_values & PLACEHOLDER_VALUES:
            raise ValueError("Production settings must not use placeholder values")

        return self

    def supabase_auth_status(self) -> str:
        required_values = {
            self.supabase_url,
            self.supabase_jwt_secret,
        }
        return "placeholder" if required_values & PLACEHOLDER_VALUES else "configured"

    def supabase_collections_storage(self) -> str:
        if self.app_env == "local":
            return "memory"

        return "supabase_rest"

    def mimoai_status(self) -> str:
        required_values = {
            self.mimoai_api_base_url,
            self.mimoai_api_key,
        }
        return "placeholder" if required_values & PLACEHOLDER_VALUES else "configured"


settings = Settings()  # type: ignore[call-arg]
