---
origem: conversa de planejamento do projeto
status: referência
data: 2026-08-27
finalidade: descrever a base fictícia de pedidos usada nos testes do agente
relacionado: [./estrutura_planilha.md](./estrutura_planilha.md) | [../data/base_ficticia_pedidos_agente_ia.xlsx](../data/base_ficticia_pedidos_agente_ia.xlsx)
---

# Sobre a Planilha — Base Fictícia de Pedidos

> Base fictícia montada no mesmo modelo das 12 colunas identificadas, estruturada de propósito para ser útil nos testes do agente.

---

## 1. Visão Geral

A base funciona como **laboratório seguro** do agente:

- Sem necessidade de VPN
- Sem ERP real
- Sem exposição de dados de clientes
- Após validação, é substituível pela fonte real (WebService do ERP) sem mudar a lógica do agente

---

## 2. Estatísticas

| Métrica | Valor |
|---|---:|
| Pedidos simulados | 120 |
| Linhas de itens | 343 |
| Clientes fictícios | 12 |
| Produtos | 22 |
| Colunas do esquema | 12 |

---

## 3. Esquema — 12 Colunas

A planilha utiliza exatamente o modelo identificado para os pedidos do projeto:

| Coluna | Significado |
|---|---|
| `PEDIDO` | Identificador do pedido |
| `CLIENTE` | Identificador do cliente |
| `QTD` | Quantidade do item no pedido |
| `COD_PROD` | Código do produto |
| `VALOR` | Valor unitário ou total do item |
| `BARCODE` | Código de barras do produto |
| `PRODUTO` | Descrição do produto |
| `MARCA` | Marca do produto |
| `REF` | Referência do fabricante |
| `SETOR` | Setor/área ao qual o produto pertence |
| `CATEGORIA` | Categoria do produto |
| `TIPO` | Tipo/subcategoria do produto |

> **Nota:** O significado exato de cada coluna está descrito tecnicamente em [`estrutura_planilha.md`](./estrutura_planilha.md).

A planilha também inclui uma aba **`LEIA_ME`** explicando como a base foi estruturada.

---

## 4. Relações Propositais

A base foi montada com combinações repetidas e intencionais para permitir **testes de recomendação**. As principais relações semânticas são:

### 4.1 Climatização

```
Ar-condicionado → suporte condensadora → cabo PP → disjuntor
```

### 4.2 Construção

```
Porcelanato → argamassa → rejunte
```

### 4.3 Eletroportáteis

```
Churrasqueira → Air Fryer → Sanduicheira
```

### 4.4 Cozinha / Eletrodomésticos

```
Cooktop → Micro-ondas → Liquidificador
```

> Os clientes apresentam **padrões de compra semelhantes, mas não idênticos**, viabilizando testes realistas de similaridade.

---

## 5. Casos de Uso Habilitados

Com essa base é possível começar a testar:

1. **Recomendação por produto adicionado**
   > *"O cliente adicionou um ar-condicionado. Quais produtos semelhantes ou complementares eu poderia sugerir?"*

2. **Recomendação por coocorrência**
   > *"Clientes que compraram este produto também costumam comprar o quê?"*

3. **Busca semântica por similaridade**
   > *"Encontre pedidos semanticamente parecidos com o pedido atual."*

---

## 6. Próximos Passos

Pipeline planejado para evolução da solução:

1. **Base fictícia** → ambiente de testes seguro
2. **Preparação dos dados** → limpeza, normalização e tipagem
3. **Embeddings / busca semântica** → indexação para RAG
4. **Agente** → núcleo agêntico com LangGraph
5. **API** → exposição via FastAPI
6. **Tomcat** → servidor de aplicação (se aplicável)
7. **Android** → cliente final (se aplicável)

> Quando o agente estiver validado na base fictícia, basta trocar a fonte de dados pela integração real (WebService do ERP) para iniciar a validação em produção.
