"""
Módulo de Utilidades - Consilius Business
Este arquivo contém funções auxiliares para formatação de dados.
Os gráficos foram removidos conforme as novas especificações institucionais.
"""

def format_currency(value):
    """
    Formata um valor numérico para o padrão de moeda brasileira (R$).
    Exemplo: 1234.56 -> R$ 1.234,56
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
