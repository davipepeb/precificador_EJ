
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from calculadora import calculate_budget, format_currency, validate_inputs, log_budget_action
from documentos import generate_proposal_pdf, generate_internal_pdf
from config import (
    HORA_PADRAO, HORAS_POR_DIA_PADRAO, DIAS_UTEIS_PADRAO, NUM_PESSOAS_PADRAO,
    SLIDER_ADICIONAL_MIN, SLIDER_ADICIONAL_MAX,
    PROPOSTA_PADRAO_PROPONENTE, AVISO_CUSTO_OPERACIONAL, AVISO_CALCULO_NECESSARIO,
    OPCOES_PAGAMENTO, MARGEM_MINIMA_DEFAULT, MARGEM_MEDIA_DEFAULT, MARGEM_NEGOCIACAO_DEFAULT,
    LOGO_PATH
)

# ==============================================================================
#                           CONFIGURAÇÃO DO STREAMLIT
# ==============================================================================

st.set_page_config(
    page_title="Sistema de Orçamentos - Consilius",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remover rodapé padrão do Streamlit e outros elementos
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            footer:after {
                content:'Sistema de Orçamento SV 1.0 - Consilius Business'; 
                visibility: visible;
                display: block;
                position: relative;
                padding: 5px;
                top: 2px;
                text-align: center;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Inicializar session state
if 'calculation_results' not in st.session_state:
    st.session_state.calculation_results = None

if 'tipo_preco_selecionado' not in st.session_state:
    st.session_state.tipo_preco_selecionado = 'Preço de negociação'

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "📊 Calculadora"

# ==============================================================================
#                           INTERFACE PRINCIPAL (LOGO À ESQUERDA)
# ==============================================================================

# Layout com logo à esquerda do título
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=120)
    else:
        st.markdown("<h1>💼</h1>", unsafe_allow_html=True)

with col_titulo:
    st.markdown(f"""
        <h1 style='margin-bottom: 0;'>Sistema de Precificação e Orçamentos</h1>
        <h3 style='margin-top: 0; color: gray;'>Consilius Business</h3>
        <p style='font-size: 1.1em;'>Gerador de Propostas Técnicas e Orçamentos</p>
        """, unsafe_allow_html=True)

st.markdown("---")

# Controle de Abas
tabs = ["📊 Calculadora", "📄 Gerar Orçamento"]
active_tab = st.radio("Navegação", tabs, index=tabs.index(st.session_state.active_tab), horizontal=True, label_visibility="collapsed")
st.session_state.active_tab = active_tab

st.markdown("---")

# ==============================================================================
#                           ABA 1: CALCULADORA
# ==============================================================================

if st.session_state.active_tab == "📊 Calculadora":
    col_inputs, col_results = st.columns([1, 1], gap="large")
    
    with col_inputs:
        st.header("Configurações")
        
        horas_por_dia = st.number_input(
            "Horas por dia", min_value=0.5, value=float(HORAS_POR_DIA_PADRAO), step=0.5
        )
        
        dias_uteis = st.number_input(
            "Dias úteis", min_value=1.0, value=float(DIAS_UTEIS_PADRAO), step=1.0
        )
        
        num_pessoas = st.number_input(
            "Número de pessoas", min_value=1.0, value=float(NUM_PESSOAS_PADRAO), step=1.0
        )
        
        valor_hora = st.number_input(
            "Valor da hora (R$)", min_value=0.0, value=float(HORA_PADRAO), step=5.0
        )
        
        custo_operacional = st.number_input(
            "Custo operacional (R$)", min_value=0.0, value=0.0, step=50.0
        )
        
        st.subheader("Ajustes")
        slider_percent = st.slider(
            "Acréscimo (%)", min_value=SLIDER_ADICIONAL_MIN, max_value=SLIDER_ADICIONAL_MAX,
            value=0.0, step=0.01
        )
        
        tipo_preco = st.selectbox(
            "Tipo de preço", ['Preço mínimo', 'Preço médio', 'Preço de negociação'],
            index=['Preço mínimo', 'Preço médio', 'Preço de negociação'].index(st.session_state.tipo_preco_selecionado)
        )
        
        if st.button("🔢 Calcular", use_container_width=True):
            is_valid, errors = validate_inputs(horas_por_dia, dias_uteis, num_pessoas, valor_hora)
            if not is_valid:
                for error in errors: st.error(error)
            else:
                results = calculate_budget(horas_por_dia, dias_uteis, num_pessoas, valor_hora, custo_operacional, slider_percent)
                st.session_state.calculation_results = results
                st.session_state.tipo_preco_selecionado = tipo_preco
                st.success("Cálculo realizado!")

        if st.button("➡️ Ir para Aba 2: Gerar Orçamento", use_container_width=True):
            if st.session_state.calculation_results:
                st.session_state.active_tab = "📄 Gerar Orçamento"
                st.rerun()
            else:
                st.error(AVISO_CALCULO_NECESSARIO)

    with col_results:
        st.header("Resultados")
        if st.session_state.calculation_results:
            res = st.session_state.calculation_results
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Mínimo", format_currency(res['precos']['minimo']))
            c2.metric("Médio", format_currency(res['precos']['medio']))
            c3.metric("Negociação", format_currency(res['precos']['negociacao']))
            
            st.markdown("---")
            st.subheader("Estatísticas")
            s1, s2 = st.columns(2)
            s1.write(f"**Total de Horas:** {res['total_horas']}h")
            s1.write(f"**Custo Trabalho:** {format_currency(res['custo_trabalho'])}")
            s2.write(f"**Custo Base:** {format_currency(res['custo_base'])}")
            s2.write(f"**Acréscimo:** {res['slider_aplicado']*100:.1f}%")
            
            st.markdown("---")
            with st.expander("🔍 Detalhamento Técnico", expanded=True):
                # Detalhamento em formato de tópicos (texto)
                st.markdown(f"""
                - **Horas por dia:** {res['inputs']['horas_por_dia']}
                - **Dias úteis:** {int(res['inputs']['dias_uteis'])}
                - **Número de pessoas:** {int(res['inputs']['num_pessoas'])}
                - **Valor da hora:** {format_currency(res['inputs']['valor_hora'])}
                - **Custo operacional:** {format_currency(res['inputs']['custo_operacional'])}
                - **Total de horas:** {res['total_horas']}
                - **Custo base:** {format_currency(res['custo_base'])}
                - **Acréscimo aplicado:** {res['slider_aplicado']*100:.1f}%
                """)
        else:
            st.info("Realize o cálculo para ver os resultados aqui.")

# ==============================================================================
#                           ABA 2: GERAR ORÇAMENTO
# ==============================================================================

elif st.session_state.active_tab == "📄 Gerar Orçamento":
    if st.session_state.calculation_results is None:
        st.error(AVISO_CALCULO_NECESSARIO)
    else:
        res = st.session_state.calculation_results
        st.header("Informações do Orçamento")
        
        col1, col2 = st.columns(2)
        with col1:
            proponente = st.text_input("Proponente", value=PROPOSTA_PADRAO_PROPONENTE)
            contratante = st.text_input("Contratante / CNPJ", placeholder="Nome da Empresa / CNPJ")
            titulo = st.text_input("Título / Tema")
        with col2:
            resumo_projeto = st.text_area("Resumo do Projeto", height=100)
        
        tipo_preco_key = st.session_state.tipo_preco_selecionado.lower().replace(" ", "_").replace("preço_", "")
        valor_selecionado = res['precos'].get(tipo_preco_key, res['precos']['negociacao'])
        st.info(f"Valor Selecionado: **{format_currency(valor_selecionado)}** ({st.session_state.tipo_preco_selecionado})")
        
        proposta_tecnica = st.text_area("Proposta Técnica", height=100)
        proposta = st.text_area("Proposta / Escopo (Etapas, Entregas, Prazos)", height=150)
        equipe = st.text_area("Equipe (Uma pessoa por linha)", height=100)
        modalidade_pagamento = st.text_area("Modalidade de Pagamento", height=80)
        opcoes_pagamento_sel = st.multiselect("Opções de Pagamento", OPCOES_PAGAMENTO, default=["Pix"])
        
        st.markdown("---")
        b1, b2 = st.columns(2)
        
        data = {
            'proponente': proponente, 'contratante': contratante, 'titulo': titulo,
            'resumo_projeto': resumo_projeto, 'proposta_tecnica': proposta_tecnica,
            'proposta': proposta, 'equipe': equipe, 'modalidade_pagamento': modalidade_pagamento,
            'opcoes_pagamento': opcoes_pagamento_sel, 'valor_selecionado': valor_selecionado,
            'valor_formatado': format_currency(valor_selecionado), 'tipo_preco_key': tipo_preco_key,
            'tipo_preco_nome': st.session_state.tipo_preco_selecionado
        }

        with b1:
            if st.button("📄 Gerar Orçamento Cliente (PDF)", use_container_width=True):
                try:
                    pdf_bytes, filename = generate_proposal_pdf(data)
                    log_budget_action(proponente, contratante, st.session_state.tipo_preco_selecionado, valor_selecionado, res)
                    st.download_button("⬇️ Baixar Orçamento", pdf_bytes, filename, "application/pdf")
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
        
        with b2:
            if st.button("📊 Gerar Documento Interno (PDF)", use_container_width=True):
                try:
                    pdf_bytes, filename = generate_internal_pdf(res, data)
                    st.download_button("⬇️ Baixar Doc Interno", pdf_bytes, filename, "application/pdf")
                except Exception as e:
                    st.error(f"Erro ao gerar PDF Interno: {e}")

# Rodapé Fixo
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Sistema de Orçamento SV 1.0<br>Consilius Business</div>", unsafe_allow_html=True)
