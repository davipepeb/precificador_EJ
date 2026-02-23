
# -*- coding: utf-8 -*-

from fpdf import FPDF
import os
from datetime import datetime
from config import RODAPE_CLIENTE, AVISO_VALOR_INDICATIVO, TEMPLATE_PATH

class PDF(FPDF):
    def __init__(self, use_template=False):
        super().__init__()
        self.use_template = use_template

    def footer(self):
        # Rodapé padrão
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        footer_text = RODAPE_CLIENTE.encode('latin-1', 'replace').decode('latin-1')
        self.cell(0, 10, footer_text, 0, 0, 'C')

    def header(self):
        if self.use_template and os.path.exists(TEMPLATE_PATH):
            # Tenta usar o template PDF como fundo (requer fpdf2 e suporte a importação)
            # Como fpdf2 puro não importa PDFs facilmente sem bibliotecas extras como pypdf,
            # vamos simular o template deixando o espaço ou usando como imagem se for convertido.
            # Se o usuário forneceu um PDF, o ideal é usar uma lib que mescle PDFs.
            pass

def safe_text(text):
    """Remove ou substitui caracteres que a fonte Arial/Helvetica do FPDF não suporta."""
    if not text: return ""
    # Substituir caracteres problemáticos
    text = text.replace('•', '-').replace('–', '-').replace('—', '-')
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_proposal_pdf(data):
    """Gera o PDF do orçamento para o cliente."""
    # Para usar um template PDF real como fundo, o ideal seria usar pypdf para mesclar.
    # Aqui vamos gerar o conteúdo e o usuário pode anexar ao template ou podemos tentar
    # uma abordagem de sobreposição se o fpdf2 permitir (com pypdf).
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Espaço inicial para o cabeçalho do template (ajustado para ~60mm)
    pdf.ln(50)
    
    # Título: Escopo
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Escopo', 0, 1, 'L')
    pdf.ln(5)
    
    # Escopo - Usando largura fixa para evitar erro de espaço horizontal
    pdf.set_font('Arial', '', 12)
    proposta_texto = data.get('proposta', '')
    effective_width = pdf.w - 2 * pdf.l_margin - 10 # Margem de segurança
    
    for line in proposta_texto.split('\n'):
        if line.strip():
            # Usar multi_cell com largura definida em vez de 0 para evitar erros de cálculo
            pdf.multi_cell(effective_width, 7, f"- {safe_text(line.strip())}")
    pdf.ln(10)
    
    # Resumo
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Resumo do Projeto', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(effective_width, 7, safe_text(data.get('resumo_projeto', '')))
    pdf.ln(5)
    
    # Investimento
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Investimento: {safe_text(data.get('valor_formatado', ''))}", 0, 1, 'L')
    pdf.set_text_color(128, 128, 128)
    pdf.set_font('Arial', 'I', 8)
    pdf.cell(0, 5, safe_text(AVISO_VALOR_INDICATIVO), 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    
    # Detalhamento
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Detalhamento', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(effective_width, 7, f"Proposta Tecnica: {safe_text(data.get('proposta_tecnica', ''))}")
    pdf.ln(5)
    
    # Pagamento
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Pagamento', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(effective_width, 7, f"Modalidade: {safe_text(data.get('modalidade_pagamento', ''))}")
    
    opcoes = data.get('opcoes_pagamento', [])
    opcoes_str = ", ".join(opcoes) if opcoes else "Nao informada"
    pdf.multi_cell(effective_width, 7, f"Opcoes aceitas: {safe_text(opcoes_str)}")
    
    cliente_sanitizado = data.get('contratante', 'Cliente').replace(' ', '_')
    filename = f"Orcamento_{cliente_sanitizado}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Se o template existir, poderíamos usar pypdf para mesclar aqui.
    # Por enquanto, geramos o PDF com o espaço correto.
    return pdf.output(), filename

def generate_internal_pdf(results, data):
    """Gera o PDF interno detalhado para a equipe."""
    pdf = PDF()
    pdf.add_page()
    effective_width = pdf.w - 2 * pdf.l_margin - 10
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'DOCUMENTO INTERNO DE PRECIFICACAO', 0, 1, 'C')
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
    pdf.ln(10)
    
    # Tabela de Dados do Projeto
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Dados do Projeto e Contratante', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    table_data = [
        ["Proponente", data.get('proponente')],
        ["Contratante", data.get('contratante')],
        ["Titulo/Tema", data.get('titulo')],
        ["Tipo de Preco Escolhido", data.get('tipo_preco_nome')],
        ["Valor Final", data.get('valor_formatado')]
    ]
    
    for row in table_data:
        pdf.cell(60, 8, safe_text(row[0]), 1)
        pdf.cell(120, 8, safe_text(row[1]), 1)
        pdf.ln()
    
    pdf.ln(10)
    
    # Tabela de Inputs Técnicos
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Memoria de Calculo (Inputs)', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    inputs = results['inputs']
    input_data = [
        ["Horas por Dia", str(inputs['horas_por_dia'])],
        ["Dias Uteis", str(int(inputs['dias_uteis']))],
        ["Numero de Pessoas", str(int(inputs['num_pessoas']))],
        ["Total de Horas", str(results['total_horas'])],
        ["Valor da Hora (R$)", f"R$ {inputs['valor_hora']:.2f}"],
        ["Custo Operacional (R$)", f"R$ {inputs['custo_operacional']:.2f}"],
        ["Acrescimo (%)", f"{inputs['slider_percent']*100:.1f}%"]
    ]
    
    for row in input_data:
        pdf.cell(60, 8, safe_text(row[0]), 1)
        pdf.cell(120, 8, safe_text(row[1]), 1)
        pdf.ln()
        
    pdf.ln(10)
    
    # Tabela de Resultados e Margens
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3. Resultados e Margens', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    precos = results['precos']
    margens = results['margens_liquidas']
    
    res_data = [
        ["Custo Base", f"R$ {results['custo_base']:.2f}"],
        ["Preco Minimo", f"R$ {precos['minimo']:.2f} (Margem: {margens['minimo']*100:.1f}%)"],
        ["Preco Medio", f"R$ {precos['medio']:.2f} (Margem: {margens['medio']*100:.1f}%)"],
        ["Preco Negociacao", f"R$ {precos['negociacao']:.2f} (Margem: {margens['negociacao']*100:.1f}%)"],
        ["Custo Hora Efetivo", f"R$ {results['custo_hora_efetivo']:.2f}"]
    ]
    
    for row in res_data:
        pdf.cell(60, 8, safe_text(row[0]), 1)
        pdf.cell(120, 8, safe_text(row[1]), 1)
        pdf.ln()

    pdf.ln(10)
    
    # Seções de Texto
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '4. Detalhes da Proposta', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    pdf.multi_cell(effective_width, 8, f"Equipe:\n{safe_text(data.get('equipe', ''))}", 1)
    pdf.ln(2)
    pdf.multi_cell(effective_width, 8, f"Modalidade de Pagamento:\n{safe_text(data.get('modalidade_pagamento', ''))}", 1)

    cliente_sanitizado = data.get('contratante', 'Interno').replace(' ', '_')
    filename = f"Interno_{cliente_sanitizado}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return pdf.output(), filename
