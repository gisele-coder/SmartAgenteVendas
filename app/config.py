from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_base_url: str = "https://opencode.ai/zen/v1"
    llm_api_key: str = ""
    llm_model: str = "hy3-free"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 3000
    llm_timeout_s: int = 30
    llm_max_retries: int = 2

    data_path: str = "data/base_ficticia_pedidos_agente_ia.xlsx"
    audit_path: str = "logs/audit.jsonl"
    log_path: str = "logs/execution.log"
    tool_delay_ms: int = 0

    flowise_alerts_enabled: bool = False
    flowise_url: str = ""
    flowise_api_key: str = ""
    flowise_chatflow_id: str = ""
    flowise_timeout_s: int = 5


settings = Settings()
