from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_base_url: str = "https://opencode.ai/zen/v1"
    llm_api_key: str = ""
    llm_model: str = "hy3-free"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 800
    llm_timeout_s: int = 30
    llm_max_retries: int = 2

    data_path: str = "data/base_ficticia_pedidos_agente_ia.xlsx"


settings = Settings()
