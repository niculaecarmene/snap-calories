"""
Configuration management using Pydantic Settings.
Loads environment variables and provides type-safe configuration access.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Settings
    environment: str = "development"
    log_level: str = "INFO"
    max_image_size_mb: int = 10
    response_timeout_seconds: int = 8

    # WhatsApp Cloud API
    whatsapp_api_token: str
    whatsapp_phone_number_id: str
    whatsapp_verify_token: str
    whatsapp_business_account_id: str

    # USDA FoodData Central API
    usda_api_key: str

    # Hugging Face (Optional)
    hugging_face_token: Optional[str] = None

    # API Base URLs
    whatsapp_api_base_url: str = "https://graph.facebook.com/v18.0"
    usda_api_base_url: str = "https://api.nal.usda.gov/fdc/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def max_image_size_bytes(self) -> int:
        """Convert MB to bytes for image size validation."""
        return self.max_image_size_mb * 1024 * 1024

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
