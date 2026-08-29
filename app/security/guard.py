import unicodedata

INJECTION_PATTERNS = (
    "ignore suas regras",
    "ignore as regras",
    "ignore previous",
    "ignore all previous",
    "desconsidere as regras",
    "desconsidere suas instrucoes",
    "instrucoes do sistema",
    "system prompt",
    "mostre todos os clientes",
    "todos os clientes e seus dados",
    "historico completo de todos",
    "histórico completo de todos",
    "revele os dados",
    "revele dados de",
    "voce e livre",
    "você é livre",
    "modo desenvolvedor",
    "jailbreak",
    "outro cliente",
    "outros clientes",
    "cliente 999999",
    "dados de outro cliente",
)

DESTRUCTIVE_PATTERNS = (
    "crie um pedido",
    "criar pedido",
    "crie pedido",
    "faça um pedido",
    "faca um pedido",
    "cancele o pedido",
    "cancelar pedido",
    "delete",
    "exclua",
    "apague",
    "remova o pedido",
    "altere o pedido",
    "modifique o pedido",
    "atualize o pedido",
    "cadastre",
    "transfira",
)


def normalize(text: str) -> str:
    lowered = text.lower().strip()
    decomposed = unicodedata.normalize("NFD", lowered)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def analyze_query(query: str) -> dict:
    normalized = normalize(query or "")
    matched_injection = [
        pattern for pattern in INJECTION_PATTERNS if normalize(pattern) in normalized
    ]
    if matched_injection:
        return {"safe": False, "kind": "injection", "patterns": matched_injection}
    matched_destructive = [
        pattern for pattern in DESTRUCTIVE_PATTERNS if normalize(pattern) in normalized
    ]
    if matched_destructive:
        return {"safe": False, "kind": "destructive", "patterns": matched_destructive}
    return {"safe": True, "kind": None, "patterns": []}
