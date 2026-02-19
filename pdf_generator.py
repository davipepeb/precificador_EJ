"""
Módulo de Geração de PDFs - Consilius Business
Este arquivo é responsável por criar os documentos PDF profissionais e internos.
Utiliza a biblioteca reportlab para gerar o conteúdo e PyPDF2 para sobrepor ao template.

COMO MODIFICAR:
- Para alterar as posições dos textos no template, edite 'pdf_layout_config.py'.
- Para alterar a logo do documento interno, substitua 'assets/logo.png'.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
import os
from pdf_layout_config import LAYOUT_ORCAMENTO, TEXT_STYLE

def get_logo_path():
    """Retorna o caminho da logo se existir."""
    path = "assets/logo.png"
    return path if os.path.exists(path) else None

def generate_client_pdf(data):
    """
    Gera o PDF de orçamento profissional sobrepondo dados ao template de 4 páginas.
    """
    template_path = "templates/template_orcamento.pdf"
    
    # Se o template não existir, gera o PDF básico anterior como fallback
    if not os.path.exists(template_path):
        return generate_fallback_client_pdf(data)
    
    # 1. Criar um PDF temporário com os textos nas posições corretas
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Configurações de estilo
    blue_color = colors.HexColor(TEXT_STYLE["color"])
    red_color = colors.HexColor(TEXT_STYLE["placeholder_color"])
    
    # --- PÁGINA 1: ESCOPO E RESUMO ---
    # Escopo
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_header"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["escopo_titulo"][1], LAYOUT_ORCAMENTO["escopo_titulo"][2], "Escopo")
    
    # Contratante
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_normal"])
    can.setFillColor(red_color)
    can.drawString(LAYOUT_ORCAMENTO["contratante"][1], LAYOUT_ORCAMENTO["contratante"][2], "Contratante: [INSIRA O NOME DO CONTRATANTE]")

    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.drawString(LAYOUT_ORCAMENTO["area"][1], LAYOUT_ORCAMENTO["area"][2], f"• Área: {data['area']}")
    can.drawString(LAYOUT_ORCAMENTO["servico"][1], LAYOUT_ORCAMENTO["servico"][2], f"• Serviço: {data['service']}")
    
    # Resumo
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.drawString(LAYOUT_ORCAMENTO["resumo_titulo"][1], LAYOUT_ORCAMENTO["resumo_titulo"][2], "Resumo do Projeto")
    
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.setFillColor(red_color)
    can.drawString(LAYOUT_ORCAMENTO["resumo_corpo"][1], LAYOUT_ORCAMENTO["resumo_corpo"][2], "[INSIRA O RESUMO DO PROJETO]")
    
    can.showPage()
    
    # --- PÁGINA 2: CONTEXTUALIZAÇÃO ---
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_header"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["contexto_titulo"][1], LAYOUT_ORCAMENTO["contexto_titulo"][2], "Contextualização")
    
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.drawString(LAYOUT_ORCAMENTO["sobre_consilius"][1], LAYOUT_ORCAMENTO["sobre_consilius"][2], "A Consilius")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.drawString(LAYOUT_ORCAMENTO["sobre_consilius"][1], LAYOUT_ORCAMENTO["sobre_consilius"][2] - 20, "Somos uma equipe ambiciosa e multidisciplinar formada por estudantes do Ibmec, atuando nas frentes administrativa, econômico-financeira e estratégica. Integramos Administração, Economia e Ciência de Dados para desenvolver soluções assertivas e orientadas por evidências. Adaptamos nossas análises e entregas à realidade de cada negócio, atuando de forma personalizada conforme suas necessidades e objetivos. Temos compromisso com excelência, responsabilidade e disciplina, assegurando entregas de qualidade e buscando sempre o melhor resultado ao nosso alcance. Nosso propósito é transformar dados em clareza, desafios em oportunidades e conhecimento em impacto real — refletindo a cultura de alto desempenho que nos forma e inspira.")
    
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.drawString(LAYOUT_ORCAMENTO["sobre_ibmec"][1], LAYOUT_ORCAMENTO["sobre_ibmec"][2], "O Ibmec")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.drawString(LAYOUT_ORCAMENTO["sobre_ibmec"][1], LAYOUT_ORCAMENTO["sobre_ibmec"][2] - 20, "Somos uma empresa júnior exclusivamente de alunos Ibmec (unidade do Distrito Federal), e atrelada à instituição, com instrução por parte dos docentes — altamente qualificados — e membros à altura do nome Ibmec, enquanto escola de negócios bem estabelecida e valorizada nacionalmente, de perfil voltado a atuação no mercado, e desenvolvimento dos estudantes por meio da prática, fornecendo contatos diretos e diferenciados com empresas, workshops, entre outros — dessa forma, incentivando contínua e diretamente as atividades da Consilius Business, enquanto empresa júnior vinculada.")
    
    can.showPage()
    
    # --- PÁGINA 3: PROPOSTA E EXECUÇÃO, EQUIPE, MODALIDADE, ETAPAS E PAGAMENTO ---
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_header"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["proposta_execucao_titulo"][1], LAYOUT_ORCAMENTO["proposta_execucao_titulo"][2], "Proposta e Execução")
    
    # Equipe
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.drawString(LAYOUT_ORCAMENTO["equipe_titulo"][1], LAYOUT_ORCAMENTO["equipe_titulo"][2], "Equipe do Projeto")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.setFillColor(red_color)
    can.drawString(LAYOUT_ORCAMENTO["equipe_corpo"][1], LAYOUT_ORCAMENTO["equipe_corpo"][2], "[INSIRA A EQUIPE DO PROJETO]")
    
    # Modalidade
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["modalidade_titulo"][1], LAYOUT_ORCAMENTO["modalidade_titulo"][2], "Modalidade de contratação")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.setFillColor(red_color)
    can.drawString(LAYOUT_ORCAMENTO["modalidade_corpo"][1], LAYOUT_ORCAMENTO["modalidade_corpo"][2], "[INSIRA A MODALIDADE DE CONTRATAÇÃO]")
    
    # Etapas
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["etapas_titulo"][1], LAYOUT_ORCAMENTO["etapas_titulo"][2], "Etapas do Projeto")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.setFillColor(red_color)
    can.drawString(LAYOUT_ORCAMENTO["etapas_corpo"][1], LAYOUT_ORCAMENTO["etapas_corpo"][2], "[INSIRA AS ETAPAS DO PROJETO]")
    
    # Pagamento
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.setFillColor(blue_color)
    can.drawString(LAYOUT_ORCAMENTO["pagamento_titulo"][1], LAYOUT_ORCAMENTO["pagamento_titulo"][2], "Pagamento:")
    can.setFont(TEXT_STYLE["font"], TEXT_STYLE["size_normal"])
    can.drawString(LAYOUT_ORCAMENTO["forma_pagamento"][1], LAYOUT_ORCAMENTO["forma_pagamento"][2], "Forma de pagamento: Pix")
    can.setFont(TEXT_STYLE["font_bold"], TEXT_STYLE["size_title"])
    can.drawString(LAYOUT_ORCAMENTO["valor_total"][1], LAYOUT_ORCAMENTO["valor_total"][2], f"Valor total (automático): R$ {data['preco_final']:,.2f}")
    
    can.showPage()
    
    can.save()
    packet.seek(0)
    
    # 2. Mesclar o PDF temporário com o template usando PyPDF2
    new_pdf = PdfReader(packet)
    template_pdf = PdfReader(open(template_path, "rb"))
    output = PdfWriter()
    
    for i in range(len(template_pdf.pages)):
        page = template_pdf.pages[i]
        if i < len(new_pdf.pages):
            page.merge_page(new_pdf.pages[i])
        output.add_page(page)
    
    # 3. Retornar o buffer final
    final_buffer = io.BytesIO()
    output.write(final_buffer)
    final_buffer.seek(0)
    return final_buffer

def generate_internal_pdf(data):
    """
    Gera o PDF de documento interno técnico (sem template).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.red,
        spaceAfter=20
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1
    )
    
    elements = []
    
    # Logo
    logo_path = get_logo_path()
    if logo_path:
        img = Image(logo_path, width=4*cm, height=2*cm)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 0.5*cm))
    
    elements.append(Paragraph("DOCUMENTO INTERNO - CONFIDENCIAL", title_style))
    elements.append(Paragraph("Memória de Cálculo de Precificação", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Dados de Entrada
    elements.append(Paragraph("<b>1. Dados de Entrada:</b>", styles['Heading3']))
    input_data = [
        ["Parâmetro", "Valor"],
        ["Área", data['area']],
        ["Serviço", data['service']],
        ["Horas Totais", f"{data['horas_totais']}h"],
        ["Horas/Dia", f"{data['horas_por_dia']}h"],
        ["Equipe Total", f"{data['total_equipe']} pessoas"],
        ["Equipe Projeto", f"{data['pessoas_projeto']} pessoas"],
        ["Custo Operacional", f"R$ {data['custo_operacional']:,.2f}"],
        ["Redutor Aplicado", f"{data['percentual_redutor']}%"]
    ]
    
    t1 = Table(input_data, colWidths=[6*cm, 9*cm])
    t1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 0.5*cm))
    
    # Multiplicadores e Fórmulas
    elements.append(Paragraph("<b>2. Multiplicadores e Índices:</b>", styles['Heading3']))
    mult_data = [
        ["Índice", "Valor", "Fórmula/Origem"],
        ["Valor Hora Base", f"R$ {data['valor_hora_base']:,.2f}", "Tabela de Áreas"],
        ["Mult. Serviço", f"{data['multiplicador_servico']}", "Tabela de Serviços"],
        ["Índice Equipe", f"{data['indice_equipe']:.3f}", "1 + 0.15 * (Pessoas/Total)"],
        ["Mult. Porte", f"{data['multiplicador_porte']}", "Seleção de Porte"],
        ["Mult. Preço", f"{data['multiplicador_preco']}", "Tipo de Preço Selecionado"]
    ]
    
    t2 = Table(mult_data, colWidths=[4*cm, 3*cm, 8*cm])
    t2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 0.5*cm))
    
    # Resultados Financeiros
    elements.append(Paragraph("<b>3. Resultados Financeiros:</b>", styles['Heading3']))
    fin_data = [
        ["Métrica", "Valor"],
        ["Valor Hora Ajustado", f"R$ {data['valor_hora_ajustado']:,.2f}"],
        ["Preço Base (1.0)", f"R$ {data['valor_base_projeto']:,.2f}"],
        ["Preço Final", f"R$ {data['preco_final']:,.2f}"],
        ["Lucro Líquido", f"R$ {data['lucro_liquido']:,.2f}"],
        ["Margem Líquida", f"{data['margem_liquida']:.2f}%"]
    ]
    
    t3 = Table(fin_data, colWidths=[6*cm, 9*cm])
    t3.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
    ]))
    elements.append(t3)
    
    # Rodapé
    elements.append(Spacer(1, 2*cm))
    elements.append(Paragraph("Consilius Business 2026 | Sistema de precificação oficial", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_fallback_client_pdf(data):
    """Fallback caso o template não seja encontrado."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = [Paragraph(f"ORÇAMENTO PROFISSIONAL - {data['service']}", styles['Heading1'])]
    elements.append(Paragraph(f"Área: {data['area']}", styles['Normal']))
    elements.append(Paragraph(f"Valor: R$ {data['preco_final']:,.2f}", styles['Normal']))
    elements.append(Paragraph("AVISO: Template 'templates/template_orcamento.pdf' não encontrado.", styles['Normal']))
    doc.build(elements)
    buffer.seek(0)
    return buffer
