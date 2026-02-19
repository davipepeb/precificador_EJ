"""
Configuração de Layout de PDF - Consilius Business
Este arquivo permite ajustar as coordenadas (x, y) de cada campo no template PDF.
As coordenadas são em pontos (1/72 polegada), começando do canto inferior esquerdo.
A4: 595 x 842 pontos.
"""

# Configurações para o Orçamento Profissional (template_orcamento.pdf)
# Cada chave representa um campo e o valor é uma tupla (página, x, y)
# Nota: A página é 0-indexada (0 = Página 1, 1 = Página 2, etc.)

LAYOUT_ORCAMENTO = {
    # PÁGINA 1 - PROPOSTA COMERCIAL, ESCOPO E RESUMO
    # Ajustado para descer o texto e evitar sobreposição ao design superior (cabeçalho verde)
    "proposta_comercial_titulo": (0, 60, 600), # Título da página
    "contratante": (0, 60, 570),
    "escopo_titulo": (0, 60, 530),
    "area": (0, 60, 510),
    "servico": (0, 60, 490),
    "resumo_titulo": (0, 60, 450),
    "resumo_corpo": (0, 60, 430),
    
    # PÁGINA 2 - CONTEXTUALIZAÇÃO (Fixo no template ou via código)
    "contexto_titulo": (1, 60, 750),
    "sobre_consilius": (1, 60, 720),
    "sobre_ibmec": (1, 60, 550),
    
    # PÁGINA 3 - PROPOSTA E EXECUÇÃO, EQUIPE, MODALIDADE, ETAPAS E PAGAMENTO
    "proposta_execucao_titulo": (2, 60, 750),
    "equipe_titulo": (2, 60, 720),
    "equipe_corpo": (2, 60, 700),
    "modalidade_titulo": (2, 60, 600),
    "modalidade_corpo": (2, 60, 580),
    "etapas_titulo": (2, 60, 500),
    "etapas_corpo": (2, 60, 480),
    "pagamento_titulo": (2, 60, 300),
    "forma_pagamento": (2, 60, 270),
    "valor_total": (2, 60, 250),
    
    # RODAPÉ FINAL (Apenas na última página de conteúdo, ex: Página 3 ou 4)
    "rodape_final": (2, 297, 50), # Centralizado na página 3 (final do conteúdo)
}

# Estilos de Texto para a sobreposição
TEXT_STYLE = {
    "font": "Helvetica",
    "font_bold": "Helvetica-Bold",
    "size_header": 18,   # Para títulos de seção
    "size_title": 12,    # Para labels
    "size_normal": 10,   # Para corpo de texto
    "color": "#1A3A5F",  # Azul institucional
    "placeholder_color": "#D32F2F"  # Vermelho para destacar placeholders
}
