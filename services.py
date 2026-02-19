"""
Módulo de Serviços - Consilius Business
Este arquivo contém a definição de todas as áreas, serviços e seus respectivos multiplicadores.
Este é o local central para adicionar novos serviços ou ajustar os valores base de precificação.

ARQUITETURA:
- SERVICES_DATA: Dicionário principal com a estrutura de preços.
- Multiplicadores de Porte e Preço: Definidos como constantes para fácil edição.
"""

# --- CONFIGURAÇÕES DE MULTIPLICADORES GLOBAIS ---
# Estes valores podem ser alterados com segurança para ajustar a política comercial da empresa.

# Multiplicador de Porte da Empresa
# Pequena -> 1.0 | Média -> 1.1 | Grande -> 1.2
PORTE_MULTIPLIERS = {
    "Pequena": 1.0,
    "Média": 1.1,
    "Grande": 1.2
}

# Multiplicadores de Tipo de Preço
# Negociação -> 1.2 | Médio -> 1.0 | Mínimo -> 0.8
PRECO_MULTIPLIERS = {
    "Negociação": 1.2,
    "Médio": 1.0,
    "Mínimo": 0.8
}

# --- BANCO DE DADOS DE ÁREAS E SERVIÇOS ---
# Estrutura:
# 'Nome da Área': {
#     'valor_hora_base': float,  # Valor base cobrado por hora nesta área
#     'servicos': {
#         'Nome do Serviço': float,  # Multiplicador de complexidade do serviço
#     }
# }

SERVICES_DATA = {
    'Administrativo': {
        'valor_hora_base': 50.0,
        'servicos': {
            'Planejamento estratégico': 1.0,
            'Organograma': 0.8,
        }
    },
    'Econômico / Estratégico': {
        'valor_hora_base': 65.0,
        'servicos': {
            'Plano estratégico de expansão de mercado': 1.2,
            'Estudo de oportunidades no mercado externo': 1.3,
            'Estudo de fornecedores': 1.0,
            'Análise de posicionamento e concorrência': 1.1,
            'Análise de precificação': 1.1,
            'Estudo de mercado e demanda': 1.2,
        }
    },
    'Financeiro': {
        'valor_hora_base': 70.0,
        'servicos': {
            'Gerenciamento de custos e precificação': 1.2,
            'Estruturação e análise de demonstrações contábeis': 1.1,
            'Valuation': 1.5,
            'Viabilidade econômico-financeira': 1.3,
            'Plano orçamentário': 1.1,
            'Análise e gerenciamento do capital de giro': 1.2,
        }
    },
    'Dados': {
        'valor_hora_base': 80.0,
        'servicos': {
            'Criação de dashboards gerenciais': 1.3,
            'Estruturação de banco de dados': 1.4,
            'Tratamento e organização de dados': 1.2,
            'Automação de relatórios': 1.3,
            'Implementação de BI': 1.5,
        }
    }
}

def get_areas():
    """
    Retorna a lista de todas as áreas disponíveis.
    Útil para preencher componentes de seleção na interface.
    """
    return list(SERVICES_DATA.keys())

def get_services_by_area(area):
    """
    Retorna a lista de serviços para uma área específica.
    """
    if area in SERVICES_DATA:
        return list(SERVICES_DATA[area]['servicos'].keys())
    return []

def get_pricing_params(area, service):
    """
    Retorna o valor_hora_base e o multiplicador_servico para uma combinação de área e serviço.
    """
    if area in SERVICES_DATA and service in SERVICES_DATA[area]['servicos']:
        base = SERVICES_DATA[area]['valor_hora_base']
        mult = SERVICES_DATA[area]['servicos'][service]
        return base, mult
    return 0.0, 0.0
