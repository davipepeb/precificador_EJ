# -*- coding: utf-8 -*-

import streamlit as st
import os
from calculadora import calculate_budget, format_currency, validate_inputs, log_budget_action, normalize_price_key
from documentos import generate_proposal_pdf, generate_internal_pdf
from config import (
    HORA_PADRAO, HORAS_POR_DIA_PADRAO, DIAS_UTEIS_PADRAO, NUM_PESSOAS_PADRAO,
    SLIDER_ADICIONAL_MIN, SLIDER_ADICIONAL_MAX,
    PROPOSTA_PADRAO_PROPONENTE, AVISO_CALCULO_NECESSARIO,
    OPCOES_PAGAMENTO, LOGO_PATH
)

st.set_page_config(
    page_title="Sistema de Orçamentos - Consilius",
    page_icon="💼",
    layout="wide"
)

if "calculation_results" not in st.session_state:
    st.session_state.calculation_results = None

if "tipo_preco_selecionado" not in st.session_state:
    st.session_state.tipo_preco_selecionado = "Preço de negociação"

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📊 Calculadora"

col_logo, col_title = st.columns([1, 5])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    else:
        st.markdown("<h1>💼</h1>", unsafe_allow_html=True)

with col_title:
    st.markdown(
        """
        <h1>Sistema de Precificação e Orçamentos</h1>
        <h3 style='color: gray;'>Consilius Business</h3>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

tabs = ["📊 Calculadora", "📄 Gerar Orçamento"]
active_tab = st.radio("", tabs, index=tabs.index(st.session_state.active_tab), horizontal=True)
st.session_state.active_tab = active_tab

st.markdown("---")

if st.session_state.active_tab == "📊 Calculadora":

    col_inputs, col_results = st.columns(2)

    with col_inputs:

        horas_por_dia = st.number_input("Horas por dia", 0.5, value=float(HORAS_POR_DIA_PADRAO), step=0.5)
        dias_uteis = st.number_input("Dias úteis", 1.0, value=float(DIAS_UTEIS_PADRAO), step=1.0)
        num_pessoas = st.number_input("Número de pessoas", 1.0, value=float(NUM_PESSOAS_PADRAO), step=1.0)
        valor_hora = st.number_input("Valor da hora (R$)", 0.0, value=float(HORA_PADRAO), step=5.0)
        custo_operacional = st.number_input("Custo operacional (R$)", 0.0, value=0.0, step=50.0)

        slider_percent = st.slider(
            "Acréscimo (%)",
            min_value=SLIDER_ADICIONAL_MIN,
            max_value=SLIDER_ADICIONAL_MAX,
            value=0.0,
            step=0.01
        )

        tipo_preco = st.selectbox(
            "Tipo de preço",
            ["Preço mínimo", "Preço médio", "Preço de negociação"],
            index=["Preço mínimo", "Preço médio", "Preço de negociação"].index(st.session_state.tipo_preco_selecionado)
        )

        if st.button("Calcular"):
            valid, errors = validate_inputs(horas_por_dia, dias_uteis, num_pessoas, valor_hora)
            if not valid:
                for e in errors:
                    st.error(e)
            else:
                st.session_state.calculation_results = calculate_budget(
                    horas_por_dia, dias_uteis, num_pessoas,
                    valor_hora, custo_operacional, slider_percent
                )
                st.session_state.tipo_preco_selecionado = tipo_preco
                st.success("Cálculo realizado")

    with col_results:
        if st.session_state.calculation_results:
            res = st.session_state.calculation_results
            st.metric("Preço Mínimo", format_currency(res["precos"]["minimo"]))
            st.metric("Preço Médio", format_currency(res["precos"]["medio"]))
            st.metric("Preço Negociação", format_currency(res["precos"]["negociacao"]))
        else:
            st.info("Realize o cálculo")

elif st.session_state.active_tab == "📄 Gerar Orçamento":

    if not st.session_state.calculation_results:
        st.error(AVISO_CALCULO_NECESSARIO)
    else:
        res = st.session_state.calculation_results

        proponente = st.text_input("Proponente", PROPOSTA_PADRAO_PROPONENTE)
        contratante = st.text_input("Contratante")
        titulo = st.text_input("Título")
        resumo = st.text_area("Resumo")
        proposta = st.text_area("Proposta")
        equipe = st.text_area("Equipe")
        pagamento = st.text_area("Modalidade de Pagamento")
        opcoes = st.multiselect("Opções", OPCOES_PAGAMENTO, default=["Pix"])

        price_key = normalize_price_key(st.session_state.tipo_preco_selecionado)
        valor = res["precos"][price_key]

        data = {
            "proponente": proponente,
            "contratante": contratante,
            "titulo": titulo,
            "resumo_projeto": resumo,
            "proposta": proposta,
            "equipe": equipe,
            "modalidade_pagamento": pagamento,
            "opcoes_pagamento": opcoes,
            "valor_formatado": format_currency(valor),
            "tipo_preco_nome": st.session_state.tipo_preco_selecionado
        }

        if st.button("Gerar PDF Cliente"):
            pdf_bytes, filename = generate_proposal_pdf(data)
            log_budget_action(proponente, contratante, st.session_state.tipo_preco_selecionado, valor, res)
            st.download_button("Download", pdf_bytes, filename, "application/pdf")

        if st.button("Gerar PDF Interno"):
            pdf_bytes, filename = generate_internal_pdf(res, data)
            st.download_button("Download Interno", pdf_bytes, filename, "application/pdf")