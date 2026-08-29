from app.tools.loader import load_orders
from app.tools.schemas import SimilarProduct

DEFAULT_LIMIT = 5


def find_similar_products(customer_id: int, limit: int = DEFAULT_LIMIT) -> list[SimilarProduct]:
    if not isinstance(customer_id, int) or customer_id <= 0:
        raise ValueError("customer_id deve ser um inteiro positivo")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit deve ser um inteiro positivo")

    df = load_orders()
    customer_orders = set(df.loc[df["cliente"] == customer_id, "pedido"].unique())
    if not customer_orders:
        return []

    customer_products = set(df.loc[df["cliente"] == customer_id, "cod_prod"].unique())
    co = df[df["pedido"].isin(customer_orders) & ~df["cod_prod"].isin(customer_products)]
    counts = co.groupby(["cod_prod", "produto"]).size().reset_index(name="cooccurrence")
    counts = counts.sort_values("cooccurrence", ascending=False).head(limit)

    total_orders = max(len(customer_orders), 1)
    return [
        SimilarProduct(
            cod_prod=int(row["cod_prod"]),
            produto=str(row["produto"]),
            cooccurrence=int(row["cooccurrence"]),
            confidence=round(min(int(row["cooccurrence"]) / total_orders, 1.0), 2),
        )
        for _, row in counts.iterrows()
    ]
