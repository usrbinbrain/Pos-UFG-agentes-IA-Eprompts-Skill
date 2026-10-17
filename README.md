
# Trabalho Disciplina de ePrompt (Pós-graduação UFG)

Este repositório contém o trabalho prático desenvolvido para a disciplina de **ePrompt** do curso de pós-graduação da **UFG** (Universidade Federal de Goiás). 

O repositório como um todo compõe a entrega do trabalho, sendo dividido em duas partes principais: o desenvolvimento de uma **Skill de Agente LLM** focada em otimização de tokens e um **Projeto Alvo (API)** utilizado para validar a execução da skill.

---

## 🧠 A Skill: Code Token Optimizer

A skill [`code-token-optimizer`](.github\skills\code-token-optimizer\SKILL.md) foi criada para instruir um agente LLM a atuar como um minificador nativo de código-fonte. 

**Principais características:**
- **Atuação In-Place:** O agente analisa e sobrescreve os arquivos originais diretamente no projeto, reduzindo o uso de tokens e o tamanho do arquivo.
- **Agent-Native:** Não utiliza formatadores, compiladores ou scripts externos (como bundlers). Todo o raciocínio de minificação segura é feito pelo próprio LLM.
- **Geração de Relatórios:** Após a execução, a skill obriga o agente a documentar as modificações no arquivo `.ai-context/minification-report.md`, detalhando os arquivos afetados, a quantidade de caracteres economizados e o percentual de redução.

---

## 🎯 Projeto Alvo de Teste: API de Cotação USD/BRL

Para demonstrar a eficácia da skill [`code-token-optimizer`](.github\skills\code-token-optimizer\SKILL.md) na prática, utilizamos como base o código desta API construída em Python com FastAPI. Ela serve para consultar a cotação entre dólar americano (USD) e real brasileiro (BRL), obtendo os dados através da [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas).

### Setup

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

```

### Executar

```bash
uvicorn api:app --reload

```

A API estará disponível em `http://127.0.0.1:8000`.

### Endpoints

#### Dólar para real

```bash
# request
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/cotacao/usd-brl?amount=10' \
  -H 'accept: */*'
```
```json
#response

{
  "from_currency": "USD",
  "to_currency": "BRL",
  "amount": "10",
  "rate": "5.0627",
  "converted_amount": "50.63",
  "source": "AwesomeAPI"
}
```

#### Real para dólar

```bash
#request
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/cotacao/brl-usd?amount=100' \
  -H 'accept: */*'

```
```json
#response

{
  "from_currency": "BRL",
  "to_currency": "USD",
  "amount": "100",
  "rate": "0.1972348",
  "converted_amount": "19.72",
  "source": "AwesomeAPI"
}
```

O parâmetro `amount` é opcional, deve ser maior que zero e tem valor padrão `1`.

### Documentação

Com a API em execução, acesse a documentação interativa gerada pelo Swagger:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

