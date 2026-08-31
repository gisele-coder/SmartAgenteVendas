import time

from app.config import settings
from app.tools.loader import load_orders
from app.tools.schemas import SimilarProduct

DEFAULT_LIMIT = 5


def find_similar_products(
    customer_id: int,
    limit: int = DEFAULT_LIMIT,
    seed_products: list[int] | None = None,
) -> list[SimilarProduct]:
    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("customer_id deve ser um inteiro positivo")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit deve ser um inteiro positivo")

    if settings.tool_delay_ms > 0:
        time.sleep(settings.tool_delay_ms / 1000)

    df = load_orders()
    seeds = {int(c) for c in (seed_products or []) if isinstance(c, int)}

    if seeds:
        orders_with_base = df.loc[df["cod_prod"].isin(seeds), "pedido"].unique()
        if len(orders_with_base) == 0:
            return []
        co = df[df["pedido"].isin(orders_with_base) & ~df["cod_prod"].isin(seeds)]
    else:
        customer_products = set(df.loc[df["cliente"] == customer_id, "cod_prod"].unique())
        if not customer_products:
            return []
        orders_with_base = df.loc[df["cod_prod"].isin(customer_products), "pedido"].unique()
        co = df[df["pedido"].isin(orders_with_base) & ~df["cod_prod"].isin(customer_products)]

    counts = co.groupby(["cod_prod", "produto"]).size().reset_index(name="cooccurrence")
    counts = counts.sort_values(["cooccurrence", "produto"], ascending=[False, True]).head(limit)
    base = max(len(orders_with_base), 1)
    return [
        SimilarProduct(
            cod_prod=int(row["cod_prod"]),
            produto=str(row["produto"]),
            cooccurrence=int(row["cooccurrence"]),
            confidence=round(min(int(row["cooccurrence"]) / base, 1.0), 2),
        )
        for _, row in counts.iterrows()
    ]
