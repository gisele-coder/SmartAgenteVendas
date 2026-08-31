from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    pedido: int = Field(..., ge=1, description="Identificador do pedido")
    cliente: int = Field(..., ge=1, description="Identificador do cliente")
    qtd: int = Field(..., ge=1, description="Quantidade do item no pedido")
    cod_prod: int = Field(..., ge=1, description="Código do produto")
    valor: float = Field(..., ge=0, description="Valor total da linha em BRL")
    barcode: str = Field(..., description="Código de barras do produto (EAN)")
    produto: str = Field(..., min_length=1, description="Descrição comercial")
    marca: str = Field(..., min_length=1, description="Marca do produto")
    ref: str = Field(..., min_length=1, description="Referência do fabricante")
    setor: str = Field(..., min_length=1, description="Setor do produto")
    categoria: str = Field(..., min_length=1, description="Categoria comercial")
    tipo: str = Field(..., min_length=1, description="Tipo/subcategoria")


class CustomerOrders(BaseModel):
    customer_id: int
    orders_count: int = Field(..., ge=0)
    items: list[OrderItem]


class SimilarProduct(BaseModel):
    cod_prod: int
    produto: str
    cooccurrence: int = Field(..., ge=0, description="Pedidos do cliente em que o produto apareceu")
    confidence: float = Field(..., ge=0, le=1, description="Coocorrência sobre total de pedidos")
