
# -*- coding: utf-8 -*-

# ==============================================================================
#                           CONFIGURAÇÕES GERAIS
# ==============================================================================

# Moeda padrão utilizada em todo o sistema
MOEDA = "BRL"
SIMBOLO_MOEDA = "R$"

# ==============================================================================
#                         CONSTANTES DE CÁLCULO PADRÃO
# ==============================================================================

# Valor padrão da hora de trabalho (em R$)
HORA_PADRAO = 20.0

# Horas padrão trabalhadas por dia
HORAS_POR_DIA_PADRAO = 2.0

# Dias úteis padrão para o cálculo
DIAS_UTEIS_PADRAO = 5.0

# Número padrão de pessoas envolvidas no projeto
NUM_PESSOAS_PADRAO = 3.0

# Removido: ADICIONAL_PADRAO (conforme novas instruções)

# ==============================================================================
#                             CONFIGURAÇÕES DE MARGEM
# ==============================================================================

# Margem mínima padrão (0%)
MARGEM_MINIMA_DEFAULT = 0.00

# Margem média padrão (10%)
MARGEM_MEDIA_DEFAULT = 0.10

# Margem de negociação padrão (15%)
MARGEM_NEGOCIACAO_DEFAULT = 0.15

# ==============================================================================
#                           CONFIGURAÇÕES DO SLIDER ADICIONAL
# ==============================================================================

# Valor mínimo para o slider de acréscimo percentual
SLIDER_ADICIONAL_MIN = 0.0

# Valor máximo para o slider de acréscimo percentual (15%)
SLIDER_ADICIONAL_MAX = 0.15

# ==============================================================================
#                           CONFIGURAÇÕES DE PROPOSTA
# ==============================================================================

# Nome padrão do proponente para a proposta
PROPOSTA_PADRAO_PROPONENTE = "Consilius Business"

# ==============================================================================
#                           TEXTOS PADRÃO E MENSAGENS
# ==============================================================================

# Mensagem de aviso para custo operacional não preenchido
AVISO_CUSTO_OPERACIONAL = "Custo operacional não preenchido. Assumindo R$ 0,00."

# Mensagem de aviso para cálculo necessário antes de gerar orçamento
AVISO_CALCULO_NECESSARIO = "É necessário gerar um cálculo na aba 'Calculadora' antes de criar o orçamento."

# Rodapé padrão para o documento do cliente
RODAPE_CLIENTE = "Consilius Business - Contato: contato@consilius.com.br - Telefone: (XX) XXXX-XXXX"

# Aviso de valor indicativo no orçamento do cliente
AVISO_VALOR_INDICATIVO = "Valor indicativo — sujeito a negociação."

# ==============================================================================
#                           OPÇÕES DE PAGAMENTO
# ==============================================================================

OPCOES_PAGAMENTO = ["Boleto", "Pix", "Transferência", "Cartão (parcela)"]

# ==============================================================================
#                           OUTRAS CONFIGURAÇÕES
# ==============================================================================

# Caminho para a logo da empresa (ex: logo.png)
# Coloque o arquivo na mesma pasta do app.py ou especifique o caminho
LOGO_PATH = "logo.png"

# Caminho para o template PDF do orçamento
TEMPLATE_PATH = "template.pdf"

# Nome do arquivo de log de orçamentos
LOG_FILE_NAME = "orcamentos_log.csv"

# Cabeçalho do arquivo de log
LOG_HEADERS = ["Timestamp", "Proponente", "Contratante", "Tipo de Preço", "Preço Final", "Custo Base", "Margem Aplicada", "Total Horas", "Custo Trabalho", "Custo Operacional", "Slider Acréscimo"]

# ==============================================================================
#                           FIM DAS CONFIGURAÇÕES
# ==============================================================================
