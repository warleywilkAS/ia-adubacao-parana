import streamlit as st
from fpdf import FPDF

# Configuração Básica
st.set_page_config(page_title="IA Adubação PR", page_icon="🌱")

# Título Simples
st.title("🌱 Recomendação de Adubação: Soja (Paraná)")

# --- ENTRADA DE DADOS ---
with st.container():
    st.subheader("Dados da Análise de Solo")
    col1, col2 = st.columns(2)
    
    with col1:
        produtor = st.text_input("Nome do Produtor", "João Silva")
        ph = st.number_input("pH em CaCl2", 0.0, 14.0, 5.2)
        argila = st.number_input("Argila (%)", 0, 100, 45)
        h_al = st.number_input("H + Al (Acidez Potencial)", 0.0, 20.0, 4.0)
        
    with col2:
        ca = st.number_input("Cálcio (Ca)", 0.0, 20.0, 3.0)
        mg = st.number_input("Magnésio (Mg)", 0.0, 10.0, 1.2)
        k = st.number_input("Potássio (K)", 0.0, 2.0, 0.2)
        prnt = st.number_input("PRNT do Calcário (%)", 1, 100, 80)

# --- CÁLCULOS ---
sb = ca + mg + k
ctc = sb + h_al
v_atual = (sb / ctc) * 100 if ctc > 0 else 0
# Meta para Soja no PR: 70%
nc = ((70 - v_atual) * ctc) / prnt if v_atual < 70 else 0

# --- EXIBIÇÃO DOS RESULTADOS ---
st.divider()
st.subheader("📋 Resultado do Diagnóstico")

if v_atual < 70:
    st.warning(f"V% Atual: {v_atual:.1f}% - Necessita de Calagem")
    st.info(f"Recomendação: {nc:.2f} toneladas/hectare")
else:
    st.success(f"V% Atual: {v_atual:.1f}% - Solo equilibrado para Soja")

# --- FUNÇÃO DO PDF ---
def gerar_pdf(nome, v, calcario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Relatorio de Recomendacao de Adubacao", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Produtor: {nome}", ln=True)
    pdf.cell(200, 10, f"Saturacao por Bases Atual: {v:.1f}%", ln=True)
    pdf.cell(200, 10, f"Necessidade de Calcario: {calcario:.2f} t/ha", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Assinatura do Tecnico: ___________________________", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# Botão para Download
if st.button("Gerar PDF"):
    pdf_bytes = gerar_pdf(produtor, v_atual, nc)
    st.download_button(
        label="📥 Baixar Relatório em PDF",
        data=pdf_bytes,
        file_name="recomendacao_soja.pdf",
        mime="application/pdf"
    )
