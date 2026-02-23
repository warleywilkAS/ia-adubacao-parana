import streamlit as st
from fpdf import FPDF
import base64

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Relatório de Adubação PR", page_icon="📄")

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatorio de Recomendacao Tecnica - Soja", ln=True, align='C')
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    for chave, valor in dados.items():
        pdf.cell(200, 10, f"{chave}: {valor}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #3e2723; color: white; }
    </style>
    """, unsafe_allow_index=True)

st.title("🌱 IA de Recomendação Paraná")

# --- INPUTS ---
with st.sidebar:
    st.header("Dados do Talhão")
    produtor = st.text_input("Nome do Produtor")
    lote = st.text_input("Identificação do Lote")

col1, col2 = st.columns(2)
with col1:
    argila = st.number_input("Argila (%)", 0, 100, 45)
    ph = st.number_input("pH (CaCl2)", 0.0, 14.0, 5.2)
    h_al = st.number_input("H + Al", 0.0, 15.0, 4.0)
with col2:
    ca = st.number_input("Cálcio (Ca)", 0.0, 20.0, 3.0)
    mg = st.number_input("Magnésio (Mg)", 0.0, 10.0, 1.2)
    k = st.number_input("Potássio (K)", 0.0, 2.0, 0.2)

# --- LÓGICA ---
sb = ca + mg + k
ctc = sb + h_al
v_atual = (sb / ctc) * 100
nc = ((70 - v_atual) * ctc) / 80 if v_atual < 70 else 0

# --- EXIBIÇÃO E PDF ---
if st.button("GERAR RECOMENDAÇÃO E PDF"):
    st.subheader("Resultado da Análise")
    st.write(f"**V% Atual:** {v_atual:.1f}%")
    st.write(f"**Necessidade de Calcário:** {nc:.2f} t/ha")
    
    # Preparar dados para o PDF
    dicionario_pdf = {
        "Produtor": produtor,
        "Lote": lote,
        "Saturacao por Bases (V%)": f"{v_atual:.1f}%",
        "Necessidade de Calcario": f"{nc:.2f} t/ha",
        "Cultura": "Soja (Manual PR)"
    }
    
    pdf_output = gerar_pdf(dicionario_pdf)
    
    st.download_button(
        label="📥 Baixar Relatório em PDF",
        data=pdf_output,
        file_name=f"Recomendacao_{produtor}.pdf",
        mime="application/pdf"
    )
