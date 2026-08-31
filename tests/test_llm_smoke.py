import pytest

from app.config import settings


@pytest.mark.skipif(not settings.llm_api_key, reason="LLM_API_KEY ausente no ambiente")
def test_llm_connectivity():
    from app.llm import get_llm

    response = get_llm().invoke("Responda apenas com a palavra: OK")
    assert "OK" in response.content
