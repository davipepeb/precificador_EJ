
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime
import os
from config import (
    MARGEM_MINIMA_DEFAULT,
    MARGEM_MEDIA_DEFAULT,
    MARGEM_NEGOCIACAO_DEFAULT,
    LOG_FILE_NAME,
    LOG_HEADERS
)

def calculate_budget(horas_por_dia, dias_uteis, num_pessoas, valor_hora, custo_operacional, slider_percent):
    """
    Realiza o cálculo completo do orçamento com base nos inputs fornecidos.
    
    Args:
        horas_por_dia (float): Horas trabalhadas por dia.
        dias_uteis (int): Total de dias úteis.
        num_pessoas (int): Número de pessoas na equipe.
        valor_hora (float): Valor da hora de trabalho.
        custo_operacional (float): Custos operacionais fixos.
        adicional (float): Valor adicional fixo.
        slider_percent (float): Percentual extra do slider (0.0 a 0.15).
        
    Returns:
        dict: Dicionário contendo todos os resultados dos cálculos.
    """
    
    # 1. Cálculo do total de horas
    total_horas = horas_por_dia * dias_uteis * num_pessoas
    
    # 2. Cálculo do custo de trabalho
    custo_trabalho = total_horas * valor_hora
    
    # 3. Cálculo do custo base (Trabalho + Operacional)
    custo_base = custo_trabalho + custo_operacional
    
    # 4. Aplicação das margens configuráveis
    # Preço Mínimo (Margem 0% por padrão)
    price_min = custo_base * (1 + MARGEM_MINIMA_DEFAULT)
    
    # Preço Médio (Margem 10% por padrão)
    price_medium = custo_base * (1 + MARGEM_MEDIA_DEFAULT)
    
    # Preço de Negociação (Margem 15% + Slider de acréscimo)
    price_negotiation = custo_base * (1 + MARGEM_NEGOCIACAO_DEFAULT + slider_percent)
    
    # 5. Cálculos Adicionais (Estatísticas)
    
    # Markup absoluto (R$) para cada preço
    markup_min = price_min - custo_base
    markup_medium = price_medium - custo_base
    markup_negotiation = price_negotiation - custo_base
    
    # Margem líquida (%) = (preço - custo_base) / preço
    # Evitar divisão por zero se o preço for 0
    margem_liq_min = (markup_min / price_min) if price_min > 0 else 0
    margem_liq_medium = (markup_medium / price_medium) if price_medium > 0 else 0
    margem_liq_negotiation = (markup_negotiation / price_negotiation) if price_negotiation > 0 else 0
    
    # Custo por hora efetivo = custo_base / total_horas
    custo_hora_efetivo = (custo_base / total_horas) if total_horas > 0 else 0
    
    # Retornar todos os dados em um dicionário estruturado
    results = {
        "total_horas": total_horas,
        "custo_trabalho": custo_trabalho,
        "custo_operacional": custo_operacional,
        "custo_base": custo_base,
        "slider_aplicado": slider_percent,
        "precos": {
            "minimo": price_min,
            "medio": price_medium,
            "negociacao": price_negotiation
        },
        "markups": {
            "minimo": markup_min,
            "medio": markup_medium,
            "negociacao": markup_negotiation
        },
        "margens_liquidas": {
            "minimo": margem_liq_min,
            "medio": margem_liq_medium,
            "negociacao": margem_liq_negotiation
        },
        "custo_hora_efetivo": custo_hora_efetivo,
        "inputs": {
            "horas_por_dia": horas_por_dia,
            "dias_uteis": dias_uteis,
            "num_pessoas": num_pessoas,
            "valor_hora": valor_hora,
            "custo_operacional": custo_operacional,
            "slider_percent": slider_percent
        }
    }
    
    return results

def format_currency(value):
    """Formata um valor numérico para o padrão de moeda R$."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def log_budget_action(proponente, contratante, tipo_preco, preco_final, results):
    """
    Registra a ação de geração de orçamento em um arquivo CSV.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_data = [
        timestamp,
        proponente,
        contratante,
        tipo_preco,
        preco_final,
        results["custo_base"],
        results["margens_liquidas"][tipo_preco.lower().replace(" ", "_").replace("é", "e").replace("í", "i")],
        results["total_horas"],
        results["custo_trabalho"],
        results["custo_operacional"],
        results["slider_aplicado"]
    ]
    
    # Criar arquivo com cabeçalho se não existir
    if not os.path.exists(LOG_FILE_NAME):
        df = pd.DataFrame([log_data], columns=LOG_HEADERS)
        df.to_csv(LOG_FILE_NAME, index=False, encoding="utf-8-sig")
    else:
        df = pd.DataFrame([log_data])
        df.to_csv(LOG_FILE_NAME, mode='a', header=False, index=False, encoding="utf-8-sig")

def validate_inputs(horas_por_dia, dias_uteis, num_pessoas, valor_hora):
    """
    Valida os inputs básicos do sistema.
    """
    errors = []
    if horas_por_dia <= 0:
        errors.append("Horas por dia deve ser maior que 0.")
    if dias_uteis <= 0:
        errors.append("Dias úteis deve ser maior que 0.")
    if num_pessoas < 1:
        errors.append("Número de pessoas deve ser pelo menos 1.")
    if valor_hora < 0:
        errors.append("Valor da hora não pode ser negativo.")
    
    return len(errors) == 0, errors

if __name__ == "__main__":
    # Teste simples conforme exemplo do prompt
    # Horas/dia = 2, Dias = 5, Pessoas = 3, Valor hora = 20, Custo operacional = 200, Adicional = 0, Slider = 0.05 (5%)
    test_results = calculate_budget(2, 5, 3, 20, 200, 0, 0.05)
    
    print(f"Total Horas: {test_results['total_horas']} (Esperado: 30)")
    print(f"Custo Trabalho: {test_results['custo_trabalho']} (Esperado: 600)")
    print(f"Custo Base: {test_results['custo_base']} (Esperado: 800)")
    print(f"Preço Mínimo: {test_results['precos']['minimo']} (Esperado: 800)")
    print(f"Preço Médio: {test_results['precos']['medio']} (Esperado: 880)")
    print(f"Preço Negociação: {test_results['precos']['negociacao']} (Esperado: 960)")
    
    assert test_results['total_horas'] == 30
    assert test_results['custo_trabalho'] == 600
    assert test_results['custo_base'] == 800
    assert test_results['precos']['minimo'] == 800
    assert test_results['precos']['medio'] == 880
    assert test_results['precos']['negociacao'] == 960
    print("Testes básicos passaram!")
