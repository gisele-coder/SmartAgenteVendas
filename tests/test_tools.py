import pytest

from app.tools import orders as orders_tool
from app.tools import similar as similar_tool
from app.tools.loader import load_orders
from app.tools.schemas import CustomerOrders, SimilarProduct

KNOWN_CLIENT = 100011
UNKNOWN_CLIENT = 999999


def test_base_carrega_com_esquema_esperado():
    df = load_orders()
    assert len(df) == 343
    assert df["pedido"].nunique() == 120
    assert df["cliente"].nunique() == 12
    assert df["cod_prod"].nunique() == 22


def test_cliente_conhecido_retorna_pedidos():
    result = orders_tool.get_customer_orders(KNOWN_CLIENT)
    assert isinstance(result, CustomerOrders)
    assert result.customer_id == KNOWN_CLIENT
    assert result.orders_count >= 1
    assert len(result.items) >= result.orders_count
    assert all(item.cliente == KNOWN_CLIENT for item in result.items)


def test_cliente_desconhecido_retorna_vazio():
    result = orders_tool.get_customer_orders(UNKNOWN_CLIENT)
    assert result.orders_count == 0
    assert result.items == []


def test_customer_exists():
    assert orders_tool.customer_exists(KNOWN_CLIENT) is True
    assert orders_tool.customer_exists(UNKNOWN_CLIENT) is False


@pytest.mark.parametrize("invalid", [0, -5])
def test_input_invalido_rejeitado(invalid):
    with pytest.raises(ValueError):
        orders_tool.get_customer_orders(invalid)
    with pytest.raises(ValueError):
        similar_tool.find_similar_products(invalid)


def test_coocorrencia_exclui_produtos_ja_comprados():
    own = {i.cod_prod for i in orders_tool.get_customer_orders(KNOWN_CLIENT).items}
    result = similar_tool.find_similar_products(KNOWN_CLIENT, limit=10)
    assert all(isinstance(s, SimilarProduct) for s in result)
    assert all(s.cod_prod not in own for s in result)
    confidences = [s.confidence for s in result]
    assert confidences == sorted(confidences, reverse=True)
    assert all(0 <= c <= 1 for c in confidences)


def test_coocorrencia_limite_respeitado():
    result = similar_tool.find_similar_products(KNOWN_CLIENT, limit=3)
    assert len(result) <= 3


def test_base_ausente_erro_claro(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "data_path", "caminho/inexistente.xlsx")
    orders_tool.load_orders.cache_clear()
    with pytest.raises(RuntimeError, match="nao encontrada"):
        orders_tool.get_customer_orders(KNOWN_CLIENT)
    orders_tool.load_orders.cache_clear()
