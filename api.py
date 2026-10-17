"""
Módulo Principal da API de Cotação de Moedas (USD/BRL) usando FastAPI.
Fornece conversões precisas de valores baseadas na taxa atual da AwesomeAPI.
"""

from decimal import Decimal, InvalidOperation
from typing import Any
import httpx
from fastapi import FastAPI, HTTPException, Query

# URL base da AwesomeAPI para buscar cotações
AWESOME_API_URL: str = "https://economia.awesomeapi.com.br/json/last"

# Inicialização da aplicação com metadados para a documentação automática
app: FastAPI = FastAPI(
    title="API de Cotação USD/BRL",
    description="Consulta cotações de dólar e real usando a AwesomeAPI.",
    version="1.0.0",
)

async def fetch_exchange_rate(pair: str) -> Decimal:
    """
    Busca a taxa de câmbio atual para o par especificado (ex: 'USD-BRL').
    Lida com a requisição HTTP, parse do JSON e extração da taxa (bid).
    """
    try:
        # Timeout de 10s previne que a API trave esperando o serviço externo
        client_timeout: float = 10.0
        
        async with httpx.AsyncClient(timeout=client_timeout) as client:
            target_url: str = f"{AWESOME_API_URL}/{pair}"
            response: httpx.Response = await client.get(target_url)
            
            # Valida o status HTTP da resposta (levanta exceção se houver erro)
            response.raise_for_status()
            
            payload: Any = response.json()
            
            # A chave da API não possui o hífen do par (ex: USD-BRL vira USDBRL)
            pair_key: str = pair.replace("-", "")
            currency_data = payload[pair_key]
            
            # Extrai o 'bid' (taxa de compra) e converte via string para manter precisão
            bid_value: str = str(currency_data["bid"])
            return Decimal(bid_value)

    # Captura possíveis erros de rede, conversão ou estrutura de dados inesperada
    except (httpx.HTTPError, KeyError, TypeError, ValueError, InvalidOperation) as error:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível consultar a cotação externa.",
        ) from error


async def quote(
    pair: str,
    from_currency: str,
    to_currency: str,
    amount: Decimal,
) -> dict[str, str]:
    """
    Orquestra a consulta da taxa e o cálculo do montante final convertido.
    Garante que os valores financeiros retornem como strings.
    """
    # Busca a taxa de conversão atual assincronamente
    fetched_rate: Decimal = await fetch_exchange_rate(pair=pair)
    
    # Multiplica o montante pela taxa obtida
    raw_amount: Decimal = amount * fetched_rate
    
    # Formata o resultado financeiro final para exatamente duas casas decimais
    quantized_amount: Decimal = raw_amount.quantize(Decimal("0.01"))
    
    # Retorna os dados estruturados, mantendo rigorosamente a compatibilidade do output
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": str(amount),
        "rate": str(fetched_rate),
        "converted_amount": str(quantized_amount),
        "source": "AwesomeAPI",
    }


@app.get("/api/v1/cotacao/usd-brl", summary="Converte USD para BRL")
async def quote_usd_to_brl(
    # Query string com validação: valor padrão de 1 e obrigatoriamente maior que 0
    amount: Decimal = Query(
        default=Decimal("1"), 
        gt=0,
        description="Montante em USD"
    ),
) -> dict[str, str]:
    """Endpoint para converter Dólar em Real."""
    return await quote(
        pair="USD-BRL",
        from_currency="USD",
        to_currency="BRL",
        amount=amount
    )


@app.get("/api/v1/cotacao/brl-usd", summary="Converte BRL para USD")
async def quote_brl_to_usd(
    # Aplica as mesmas validações rigorosas da rota anterior
    amount: Decimal = Query(
        default=Decimal("1"), 
        gt=0,
        description="Montante em BRL"
    ),
) -> dict[str, str]:
    """Endpoint para converter Real em Dólar."""
    return await quote(
        pair="BRL-USD",
        from_currency="BRL",
        to_currency="USD",
        amount=amount
    )