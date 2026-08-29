from functools import lru_cache

import pandas as pd

from app.config import settings

EXPECTED_COLUMNS = {
    "PEDIDO",
    "CLIENTE",
    "QTD",
    "COD_PROD",
    "VALOR",
    "BARCODE",
    "PRODUTO",
    "MARCA",
    "REF",
    "SETOR",
    "CATEGORIA",
    "TIPO",
}
SHEET_NAME = "PEDIDOS"


@lru_cache(maxsize=1)
def load_orders() -> pd.DataFrame:
    try:
        df = pd.read_excel(settings.data_path, sheet_name=SHEET_NAME)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Base de dados nao encontrada: {settings.data_path}") from exc
    except ValueError as exc:
        raise RuntimeError(f"Aba '{SHEET_NAME}' ausente na base: {exc}") from exc

    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        raise RuntimeError(f"Colunas ausentes na base: {sorted(missing)}")

    df.columns = [str(c).lower() for c in df.columns]
    return df
