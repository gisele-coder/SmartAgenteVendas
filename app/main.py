from fastapi import FastAPI

app = FastAPI(
    title="SmartOrder AI",
    description="Agente Inteligente de Pedidos e Recomendações",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "smartorder-ai"}
