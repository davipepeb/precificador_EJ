"""
Módulo de Precificação - Consilius Business
Este arquivo contém toda a lógica matemática para o cálculo de orçamentos.
As fórmulas aqui implementadas seguem as diretrizes institucionais da empresa júnior.

COMO MODIFICAR:
- Para alterar a fórmula do índice de equipe, modifique a variável 'indice_equipe'.
- Para alterar a lógica do redutor, modifique a variável 'multiplicador_redutor'.
"""

def calculate_pricing(
    valor_hora_base,
    multiplicador_servico,
    horas_por_dia,
    horas_totais,
    total_equipe,
    pessoas_projeto,
    multiplicador_porte,
    percentual_redutor,
    custo_operacional,
    multiplicador_preco
):
    """
    Calcula todos os valores financeiros e operacionais do projeto.
    
    Inputs:
        valor_hora_base (float): Valor base por hora da área selecionada.
        multiplicador_servico (float): Multiplicador de complexidade do serviço.
        horas_por_dia (float): Horas de trabalho diárias estimadas.
        horas_totais (float): Total de horas estimadas para o projeto.
        total_equipe (int): Número total de membros na empresa júnior.
        pessoas_projeto (int): Número de membros alocados neste projeto.
        multiplicador_porte (float): Multiplicador baseado no porte da empresa cliente.
        percentual_redutor (float): Desconto percentual aplicado (0-100).
        custo_operacional (float): Custos fixos/variáveis em reais para o projeto.
        multiplicador_preco (float): Multiplicador do tipo de preço (Negociação, Médio, Mínimo).
        
    Outputs:
        dict: Dicionário contendo todos os resultados calculados.
    """
    
    # 1. Valor hora ajustado pelo serviço
    # Multiplica o valor base da área pela complexidade do serviço específico.
    valor_hora_ajustado = valor_hora_base * multiplicador_servico
    
    # 2. Dias estimados de projeto
    # Divide o total de horas pelas horas trabalhadas por dia.
    # Evita divisão por zero se horas_por_dia for 0.
    dias_projeto = horas_totais / horas_por_dia if horas_por_dia > 0 else 0
    
    # 3. Índice de equipe
    # Fórmula institucional: 1 + 0.15 * (pessoas_projeto / total_equipe)
    # Limitado entre 1.00 e 1.15 para garantir equilíbrio na precificação.
    if total_equipe > 0:
        indice_equipe = 1 + 0.15 * (pessoas_projeto / total_equipe)
    else:
        indice_equipe = 1.0
    
    indice_equipe = max(1.00, min(1.15, indice_equipe))
    
    # 4. Multiplicador redutor (desconto)
    # Converte o percentual (ex: 50) em um multiplicador (ex: 0.5).
    # Fórmula: 1 - percentual / 100
    multiplicador_redutor = 1 - (percentual_redutor / 100)
    
    # 5. Valor base do projeto (Cálculo principal)
    # Combina todos os fatores para chegar ao preço base (1.0).
    valor_base_projeto = (
        valor_hora_ajustado * 
        horas_totais * 
        multiplicador_porte * 
        indice_equipe * 
        multiplicador_redutor
    )
    
    # 6. Preços por categoria (Cenários de Negociação)
    # Estes valores são calculados para dar opções ao consultor durante a venda.
    preco_negociacao = valor_base_projeto * 1.20
    preco_medio = valor_base_projeto * 1.00
    preco_minimo = valor_base_projeto * 0.80
    
    # 7. Preço final selecionado
    # Aplica o multiplicador do tipo de preço escolhido pelo usuário.
    preco_final = valor_base_projeto * multiplicador_preco
    
    # 8. Lucro e Margem
    # Lucro Líquido = Preço Final - Custos Operacionais
    lucro_liquido = preco_final - custo_operacional
    # Margem Líquida = (Lucro / Preço Final) * 100
    # Evita divisão por zero se preco_final for 0.
    margem_liquida = (lucro_liquido / preco_final * 100) if preco_final > 0 else 0
    
    return {
        'valor_hora_ajustado': valor_hora_ajustado,
        'dias_projeto': dias_projeto,
        'indice_equipe': indice_equipe,
        'multiplicador_redutor': multiplicador_redutor,
        'valor_base_projeto': valor_base_projeto,
        'preco_negociacao': preco_negociacao,
        'preco_medio': preco_medio,
        'preco_minimo': preco_minimo,
        'preco_final': preco_final,
        'lucro_liquido': lucro_liquido,
        'margem_liquida': margem_liquida
    }
