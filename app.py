"""
Aplicação Principal - Consilius Business
Este arquivo contém a interface Streamlit para o sistema de precificação.
Ele integra todos os módulos para proporcionar uma experiência profissional.

REQUISITOS IMPLEMENTADOS:
- Logo pequena no canto superior esquerdo (complemento visual).
- Título "Sistema de Precificação Consilius Business" preservado.
- Visibilidade controlada por st.session_state.
- CSS customizado para Dark/Light mode.
"""

import streamlit as st
import pandas as pd
import os
from services import get_areas, get_services_by_area, get_pricing_params, PORTE_MULTIPLIERS, PRECO_MULTIPLIERS
from pricing import calculate_pricing
from pdf_generator import generate_client_pdf, generate_internal_pdf
from utils import format_currency

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Consilius Business - Precificação",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Estilização das métricas em destaque */
    .metric-container {
        background-color: rgba(26, 58, 95, 0.1);
        border: 2px solid #1A3A5F;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2.2em;
        font-weight: bold;
        color: #1A3A5F;
    }
    .metric-label {
        font-size: 1.1em;
        color: #555;
        margin-bottom: 5px;
    }
    
    /* Ajuste para Dark Mode */
    @media (prefers-color-scheme: dark) {
        .metric-container {
            background-color: rgba(255, 255, 255, 0.05);
            border-color: #4A90E2;
        }
        .metric-value {
            color: #4A90E2;
        }
        .metric-label {
            color: #CCC;
        }
    }

    /* Botão Calcular */
    .stButton>button {
        width: 100%;
        background-color: #1A3A5F;
        color: white;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
        font-size: 1.1em;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2E5A88;
        border-color: #1A3A5F;
    }

    /* Rodapé Fixo */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #555;
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        border-top: 1px solid #ddd;
        z-index: 999;
    }
    @media (prefers-color-scheme: dark) {
        .footer {
            background-color: #1e1e1e;
            color: #aaa;
            border-top: 1px solid #333;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO (SESSION STATE) ---
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'results' not in st.session_state:
    st.session_state.results = None

# --- CABEÇALHO COM LOGO PEQUENA E TÍTULO ---
# Logo pequena no canto superior esquerdo como complemento visual
col_header_1, col_header_2 = st.columns([0.15, 1])
with col_header_1:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=80) # Logo pequena (80px)
with col_header_2:
    st.title("Sistema de Precificação Consilius Business")

st.markdown("---")

# --- LAYOUT PRINCIPAL ---
col_left, col_right = st.columns([1, 1.2], gap="large")

with col_left:
    st.subheader("🛠️ Configurações do Projeto")
    
    # 1. Seleção de Área e Serviço
    area_selecionada = st.selectbox("Selecione a Área", get_areas())
    servicos_disponiveis = get_services_by_area(area_selecionada)
    servico_selecionado = st.selectbox("Selecione o Serviço", servicos_disponiveis)
    
    # Obtém parâmetros base do serviço
    valor_hora_base, multiplicador_servico = get_pricing_params(area_selecionada, servico_selecionado)
    
    # 2. Inputs Operacionais
    st.markdown("### Operacional")
    c1, c2 = st.columns(2)
    with c1:
        horas_por_dia = st.number_input("Horas por dia", min_value=0.1, value=1.0, step=0.5)
        total_equipe = st.number_input("Total de pessoas na equipe", min_value=1, value=5)
    with c2:
        horas_totais = st.number_input("Horas totais do projeto", min_value=1.0, value=30.0, step=1.0)
        pessoas_projeto = st.number_input("Pessoas alocadas no projeto", min_value=1, value=3)
    
    # 3. Inputs de Negócio
    st.markdown("### Negócio")
    c3, c4 = st.columns(2)
    with c3:
        porte_empresa = st.selectbox("Porte da Empresa", list(PORTE_MULTIPLIERS.keys()), index=0) # Default: Pequena
        multiplicador_porte = PORTE_MULTIPLIERS[porte_empresa]
        percentual_redutor = st.number_input("Redutor percentual (%)", min_value=0, max_value=100, value=50)
        
    with c4:
        tipo_preco = st.selectbox("Tipo de Preço", list(PRECO_MULTIPLIERS.keys()), index=0) # Default: Negociação
        multiplicador_preco = PRECO_MULTIPLIERS[tipo_preco]
        custo_operacional = st.number_input("Custo operacional (R$)", min_value=0.0, value=0.0, step=50.0)

    # Botão de Cálculo
    if st.button("CALCULAR ORÇAMENTO"):
        st.session_state.results = calculate_pricing(
            valor_hora_base,
            multiplicador_servico,
            horas_por_dia,
            horas_totais,
            total_equipe,
            pessoas_projeto,
            multiplicador_porte,
            percentual_redutor,
            custo_operacional,
            multiplicador_preco
        )
        st.session_state.calculated = True
        st.session_state.inputs = {
            'area': area_selecionada,
            'service': servico_selecionado,
            'valor_hora_base': valor_hora_base,
            'multiplicador_servico': multiplicador_servico,
            'horas_por_dia': horas_por_dia,
            'horas_totais': horas_totais,
            'total_equipe': total_equipe,
            'pessoas_projeto': pessoas_projeto,
            'multiplicador_porte': multiplicador_porte,
            'percentual_redutor': percentual_redutor,
            'custo_operacional': custo_operacional,
            'multiplicador_preco': multiplicador_preco
        }

with col_right:
    if st.session_state.calculated:
        res = st.session_state.results
        inp = st.session_state.inputs
        
        st.subheader("📈 Detalhes técnicos e downloads")
        
        # Destaque Visual
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="metric-container"><div class="metric-label">Preço Final</div><div class="metric-value">{format_currency(res['preco_final'])}</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="metric-container"><div class="metric-label">Margem Líquida</div><div class="metric-value">{res['margem_liquida']:.1f}%</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="metric-container"><div class="metric-label">Prazo Estimado</div><div class="metric-value">{res['dias_projeto']:.1f} dias</div></div>""", unsafe_allow_html=True)
        
        # Detalhes Técnicos
        with st.expander("Ver Detalhamento Técnico Completo", expanded=True):
            st.markdown(f"""
            - **Área:** {inp['area']}
            - **Serviço:** {inp['service']}
            - **Valor Hora Base:** {format_currency(inp['valor_hora_base'])}
            - **Valor Hora Ajustado:** {format_currency(res['valor_hora_ajustado'])}
            - **Horas Totais:** {inp['horas_totais']}h
            - **Dias Estimados:** {res['dias_projeto']:.1f} dias
            - **Índice Equipe:** {res['indice_equipe']:.3f}
            - **Redutor Aplicado:** {inp['percentual_redutor']}%
            - **Valor Base do Projeto:** {format_currency(res['valor_base_projeto'])}
            - **Preço Negociação:** {format_currency(res['preco_negociacao'])}
            - **Preço Médio:** {format_currency(res['preco_medio'])}
            - **Preço Mínimo:** {format_currency(res['preco_minimo'])}
            - **Preço Final Selecionado:** {format_currency(res['preco_final'])}
            - **Margem Líquida:** {res['margem_liquida']:.2f}%
            """)
        
        # Botões de Download
        st.markdown("### 📥 Downloads")
        pdf_data = {**inp, **res}
        
        d_col1, d_col2 = st.columns(2)
        with d_col1:
            client_pdf = generate_client_pdf(pdf_data)
            st.download_button(
                label="📄 Baixar Orçamento Profissional",
                data=client_pdf,
                file_name=f"Orcamento_{inp['service'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        with d_col2:
            internal_pdf = generate_internal_pdf(pdf_data)
            st.download_button(
                label="🔒 Baixar Documento Interno",
                data=internal_pdf,
                file_name=f"Interno_{inp['service'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Configure os parâmetros à esquerda e clique em 'Calcular orçamento' para visualizar os resultados e baixar os documentos.")

# --- RODAPÉ FIXO ---
st.markdown("""
    <div class="footer">
        Consilius Business 2026 | Sistema de precificação oficial
    </div>
    """, unsafe_allow_html=True)
