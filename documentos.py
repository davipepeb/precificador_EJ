# -*- coding: utf-8 -*-

from fpdf import FPDF
from datetime import datetime
from config import RODAPE_CLIENTE, AVISO_VALOR_INDICATIVO


PAGE_MARGIN = 20
CONTENT_WIDTH = 170  # largura fixa segura para A4


class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, _safe_text(RODAPE_CLIENTE), 0, 0, "C")


def _safe_text(text):
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def _pdf_to_bytes(pdf):
    content = pdf.output(dest="S")
    if isinstance(content, (bytes, bytearray)):
        return bytes(content)
    return content.encode("latin-1", errors="replace")


def _write_block(pdf, text, size=11, bold=False):
    pdf.set_x(PAGE_MARGIN)
    pdf.set_font("Arial", "B" if bold else "", size)
    pdf.multi_cell(CONTENT_WIDTH, 6, _safe_text(text))
    pdf.ln(2)


# ==============================
# PDF CLIENTE
# ==============================

def generate_proposal_pdf(data):

    pdf = PDF("P", "mm", "A4")
    pdf.set_margins(PAGE_MARGIN, PAGE_MARGIN, PAGE_MARGIN)
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "PROPOSTA COMERCIAL", ln=1, align="C")
    pdf.ln(8)

    _write_block(pdf, "Informações Gerais", 13, True)

    _write_block(pdf, f"Proponente: {data.get('proponente','')}")
    _write_block(pdf, f"Contratante: {data.get('contratante','')}")
    _write_block(pdf, f"Título: {data.get('titulo','')}")

    pdf.ln(4)

    _write_block(pdf, "Resumo do Projeto", 13, True)
    _write_block(pdf, data.get("resumo_projeto", ""))

    pdf.ln(4)

    _write_block(pdf, "Escopo / Proposta", 13, True)
    _write_block(pdf, data.get("proposta", ""))

    pdf.ln(4)

    _write_block(pdf, "Equipe", 13, True)
    _write_block(pdf, data.get("equipe", ""))

    pdf.ln(4)

    _write_block(pdf, "Condições Comerciais", 13, True)
    _write_block(pdf, data.get("modalidade_pagamento", ""))

    opcoes = data.get("opcoes_pagamento", [])
    if isinstance(opcoes, list):
        opcoes = ", ".join(opcoes)

    _write_block(pdf, f"Opções aceitas: {opcoes}")

    pdf.ln(6)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Investimento: {_safe_text(data.get('valor_formatado',''))}", ln=1, align="C")

    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, _safe_text(AVISO_VALOR_INDICATIVO), ln=1, align="C")

    filename = f"Orcamento_{datetime.now().strftime('%Y%m%d')}.pdf"
    return _pdf_to_bytes(pdf), filename


# ==============================
# PDF INTERNO
# ==============================

def generate_internal_pdf(results, data):

    pdf = PDF("P", "mm", "A4")
    pdf.set_margins(PAGE_MARGIN, PAGE_MARGIN, PAGE_MARGIN)
    pdf.add_page()

    pdf.set_font("Arial", "B", 17)
    pdf.cell(0, 10, "DOCUMENTO INTERNO DE PRECIFICAÇÃO", ln=1, align="C")
    pdf.ln(8)

    _write_block(pdf, "Dados do Projeto", 13, True)

    _write_block(pdf, f"Proponente: {data.get('proponente','')}")
    _write_block(pdf, f"Contratante: {data.get('contratante','')}")
    _write_block(pdf, f"Título: {data.get('titulo','')}")
    _write_block(pdf, f"Tipo de Preço: {data.get('tipo_preco_nome','')}")

    pdf.ln(6)

    _write_block(pdf, "Memória de Cálculo", 13, True)

    _write_block(pdf, f"Custo Base: R$ {results['custo_base']:.2f}")
    _write_block(pdf, f"Total Horas: {results['total_horas']}")
    _write_block(pdf, f"Custo Trabalho: R$ {results['custo_trabalho']:.2f}")
    _write_block(pdf, f"Custo Operacional: R$ {results['custo_operacional']:.2f}")
    _write_block(pdf, f"Acréscimo Slider: {results['slider_aplicado']*100:.1f}%")

    pdf.ln(6)

    _write_block(pdf, "Resultados", 13, True)

    _write_block(pdf, f"Preço Mínimo: R$ {results['precos']['minimo']:.2f}")
    _write_block(pdf, f"Preço Médio: R$ {results['precos']['medio']:.2f}")
    _write_block(pdf, f"Preço Negociação: R$ {results['precos']['negociacao']:.2f}")

    filename = f"Interno_{datetime.now().strftime('%Y%m%d')}.pdf"
    return _pdf_to_bytes(pdf), filename