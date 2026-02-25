# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os
import unicodedata
from config import (
    MARGEM_MINIMA_DEFAULT,
    MARGEM_MEDIA_DEFAULT,
    MARGEM_NEGOCIACAO_DEFAULT,
    LOG_FILE_NAME,
    LOG_HEADERS
)

def _strip_accents(text):
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))

def normalize_price_key(label):
    raw = _strip_accents(label).lower()
    if "minim" in raw:
        return "minimo"
    if "medi" in raw:
        return "medio"
    return "negociacao"

def calculate_budget(horas_por_dia, dias_uteis, num_pessoas, valor_hora, custo_operacional, slider_percent):
    total_horas = horas_por_dia * dias_uteis * num_pessoas
    custo_trabalho = total_horas * valor_hora
    custo_base = custo_trabalho + custo_operacional

    price_min = custo_base * (1 + MARGEM_MINIMA_DEFAULT)
    price_med = custo_base * (1 + MARGEM_MEDIA_DEFAULT)
    price_neg = custo_base * (1 + MARGEM_NEGOCIACAO_DEFAULT + slider_percent)

    return {
        "total_horas": total_horas,
        "custo_trabalho": custo_trabalho,
        "custo_operacional": custo_operacional,
        "custo_base": custo_base,
        "slider_aplicado": slider_percent,
        "precos": {
            "minimo": price_min,
            "medio": price_med,
            "negociacao": price_neg
        },
        "margens_liquidas": {
            "minimo": (price_min - custo_base) / price_min if price_min else 0,
            "medio": (price_med - custo_base) / price_med if price_med else 0,
            "negociacao": (price_neg - custo_base) / price_neg if price_neg else 0
        },
        "inputs": {
            "horas_por_dia": horas_por_dia,
            "dias_uteis": dias_uteis,
            "num_pessoas": num_pessoas,
            "valor_hora": valor_hora,
            "custo_operacional": custo_operacional,
            "slider_percent": slider_percent
        }
    }

def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def log_budget_action(proponente, contratante, tipo_preco, preco_final, results):
    key = normalize_price_key(tipo_preco)
    margin = results["margens_liquidas"][key]

    data = [[
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        proponente,
        contratante,
        tipo_preco,
        preco_final,
        results["custo_base"],
        margin,
        results["total_horas"],
        results["custo_trabalho"],
        results["custo_operacional"],
        results["slider_aplicado"]
    ]]

    if not os.path.exists(LOG_FILE_NAME):
        pd.DataFrame(data, columns=LOG_HEADERS).to_csv(LOG_FILE_NAME, index=False)
    else:
        pd.DataFrame(data).to_csv(LOG_FILE_NAME, mode="a", header=False, index=False)

def validate_inputs(horas_por_dia, dias_uteis, num_pessoas, valor_hora):
    errors = []
    if horas_por_dia <= 0: errors.append("Horas por dia deve ser maior que 0")
    if dias_uteis <= 0: errors.append("Dias úteis deve ser maior que 0")
    if num_pessoas < 1: errors.append("Número de pessoas inválido")
    if valor_hora < 0: errors.append("Valor da hora inválido")
    return len(errors) == 0, errors