# -*- coding: utf-8 -*-

from fpdf import FPDF
from datetime import datetime
from config import RODAPE_CLIENTE, AVISO_VALOR_INDICATIVO


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, _safe_text(RODAPE_CLIENTE), 0, 0, "C")


def _safe_text(text):
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def _pdf_to_bytes(pdf: FPDF) -> bytes:
    content = pdf.output(dest="S")
    if isinstance(content, (bytes, bytearray)):
        return bytes(content)
    if isinstance(content, str):
        return content.encode("latin-1", errors="replace")
    raise TypeError(f"Unsupported PDF output type: {type(content)}")


def _effective_width(pdf: FPDF) -> float:
    return float(pdf.w - pdf.l_margin - pdf.r_margin)


def _newline(pdf: FPDF, h: float):
    pdf.set_x(pdf.l_margin)
    pdf.set_y(pdf.get_y() + h)


def _write_multicell(pdf: FPDF, text: str, line_height: float = 6.5):
    pdf.set_x(pdf.l_margin)
    w = _effective_width(pdf)
    if w <= 1:
        pdf.set_x(pdf.l_margin)
        w = _effective_width(pdf)
    pdf.multi_cell(w, line_height, _safe_text(text), align="L")
    pdf.set_x(pdf.l_margin)


def generate_proposal_pdf(data):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.set_x(pdf.l_margin)
    pdf.cell(_effective_width(pdf), 10, "Orçamento", ln=1)

    _newline(pdf, 2)

    pdf.set_font("Arial", "", 12)
    _write_multicell(pdf, f"Proponente: {data.get('proponente', '')}")
    _write_multicell(pdf, f"Contratante: {data.get('contratante', '')}")
    _write_multicell(pdf, f"Título: {data.get('titulo', '')}")

    _newline(pdf, 2)

    _write_multicell(pdf, "Resumo do Projeto:")
    _write_multicell(pdf, data.get("resumo_projeto", ""))

    _newline(pdf, 2)

    pdf.set_font("Arial", "B", 12)
    _write_multicell(pdf, f"Valor: {data.get('valor_formatado', '')}")

    pdf.set_font("Arial", "I", 9)
    _write_multicell(pdf, AVISO_VALOR_INDICATIVO)

    filename = f"Orcamento_{datetime.now().strftime('%Y%m%d')}.pdf"
    return _pdf_to_bytes(pdf), filename


def generate_internal_pdf(results, data):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.set_x(pdf.l_margin)
    pdf.cell(_effective_width(pdf), 10, "Documento Interno de Precificação", ln=1)

    _newline(pdf, 2)

    pdf.set_font("Arial", "", 11)

    _write_multicell(pdf, f"Proponente: {data.get('proponente', '')}")
    _write_multicell(pdf, f"Contratante: {data.get('contratante', '')}")
    _write_multicell(pdf, f"Título: {data.get('titulo', '')}")
    _write_multicell(pdf, f"Tipo de Preço: {data.get('tipo_preco_nome', '')}")

    _newline(pdf, 2)

    _write_multicell(pdf, f"Custo Base: R$ {results['custo_base']:.2f}")
    _write_multicell(pdf, f"Total Horas: {results['total_horas']}")
    _write_multicell(pdf, f"Custo Trabalho: R$ {results['custo_trabalho']:.2f}")
    _write_multicell(pdf, f"Custo Operacional: R$ {results['custo_operacional']:.2f}")
    _write_multicell(pdf, f"Acréscimo Slider: {results['slider_aplicado']*100:.1f}%")

    _newline(pdf, 2)

    _write_multicell(pdf, f"Preço Mínimo: R$ {results['precos']['minimo']:.2f}")
    _write_multicell(pdf, f"Preço Médio: R$ {results['precos']['medio']:.2f}")
    _write_multicell(pdf, f"Preço Negociação: R$ {results['precos']['negociacao']:.2f}")

    filename = f"Interno_{datetime.now().strftime('%Y%m%d')}.pdf"
    return _pdf_to_bytes(pdf), filename