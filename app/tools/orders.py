import pandas as pd

from app.tools.loader import load_orders
from app.tools.schemas import CustomerOrders, OrderItem


def _to_item(row: pd.Series) -> OrderItem:
    return OrderItem(
        pedido=int(row["pedido"]),
        cliente=int(row["cliente"]),
        qtd=int(row["qtd"]),
        cod_prod=int(row["cod_prod"]),
        valor=float(row["valor"]),
        barcode=str(row["barcode"]),
        produto=str(row["produto"]),
        marca=str(row["marca"]),
        ref=str(row["ref"]),
        setor=str(row["setor"]),
        categoria=str(row["categoria"]),
        tipo=str(row["tipo"]),
    )


def customer_exists(customer_id: int) -> bool:
    df = load_orders()
    return bool((df["cliente"] == customer_id).any())


def get_customer_orders(customer_id: int) -> CustomerOrders:
    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("customer_id deve ser um inteiro positivo")

    df = load_orders()
    rows = df[df["cliente"] == customer_id]
    items = [_to_item(row) for _, row in rows.iterrows()]
    return CustomerOrders(
        customer_id=customer_id,
        orders_count=int(rows["pedido"].nunique()),
        items=items,
    )
