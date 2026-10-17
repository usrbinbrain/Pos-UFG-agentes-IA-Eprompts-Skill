from decimal import Decimal, InvalidOperation
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query

AWESOME_API_URL = "https://economia.awesomeapi.com.br/json/last"

app = FastAPI(
    title="API de Cotação USD/BRL",
    description="Consulta cotações de dólar e real usando a AwesomeAPI.",
    version="1.0.0",
)


async def fetch_exchange_rate(pair: str) -> Decimal:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{AWESOME_API_URL}/{pair}")
            response.raise_for_status()
            payload: Any = response.json()
            bid = payload[pair.replace("-", "")]
            return Decimal(str(bid["bid"]))
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
    rate = await fetch_exchange_rate(pair)
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": str(amount),
        "rate": str(rate),
        "converted_amount": str((amount * rate).quantize(Decimal("0.01"))),
        "source": "AwesomeAPI",
    }


@app.get("/api/v1/cotacao/usd-brl")
async def quote_usd_to_brl(
    amount: Decimal = Query(default=Decimal("1"), gt=0),
) -> dict[str, str]:
    return await quote("USD-BRL", "USD", "BRL", amount)


@app.get("/api/v1/cotacao/brl-usd")
async def quote_brl_to_usd(
    amount: Decimal = Query(default=Decimal("1"), gt=0),
) -> dict[str, str]:
    return await quote("BRL-USD", "BRL", "USD", amount)
