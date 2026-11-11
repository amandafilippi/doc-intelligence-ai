import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
import google.generativeai as genai

# 1. Configuração da página Streamlit
st.set_page_config(
    page_title="DocIntelligence AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocIntelligence AI")
st.caption("Análise automatizada de contratos, editais e documentos corporativos com IA")

# 2. Carregar variáveis de ambiente e Chave de API
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

if not api_key:
    st.error("⚠️ Chave de API não encontrada! Configure a variável GEMINI_API_KEY no arquivo .env.")
    st.stop()

# Configura a chave de API na biblioteca
genai.configure(api_key=api_key)

# Instancia o modelo com a versão estável aceita pela API
model = genai.GenerativeModel('models/gemini-3.8-flash')

# 3. Função para extrair texto de PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

# 4. Função de análise com a IA
def analyze_document(doc_text):
    prompt = f"""
    Analise o documento fornecido abaixo e forneça um relatório estruturado estritamente no seguinte formato Markdown:

    ### 📌 Resumo Executivo
    Forneça uma síntese clara em 3 a 5 tópicos principais explicando do que se trata o documento, partes envolvidas e objetivo principal.

    ### 🔍 Fatos & Dados Principais
    - **Datas Importantes:** [Datas encontradas ou 'Não especificadas']
    - **Valores/Montantes:** [Valores financeiros ou 'Não especificados']
    - **Vigência/Prazos:** [Informações sobre prazos]

    ### ⚠️ Análise de Riscos e Inconsistências
    Liste em marcadores (com alertas em negrito) os pontos de atenção, cláusulas de alto risco, ambiguidades ou ausência de informações críticas que deveriam estar presentes.

    ---
    DOCUMENTO PARA ANÁLISE:
    {doc_text[:15000]}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Erro na comunicação com a IA: {str(e)}"

# 5. Interface Lateral (Sidebar)
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    uploaded_file = st.file_uploader("Faça upload de um arquivo PDF", type=["pdf"])
    st.info("💡 **Dica de uso:** Suba minutas de contratos, termos de referência, editais ou relatórios de processos.")

# 6. Gerenciamento do estado da aplicação
if "doc_text" not in st.session_state:
    st.session_state.doc_text = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Processar upload
if uploaded_file:
    with st.spinner("Extraindo texto do PDF..."):
        st.session_state.doc_text = extract_text_from_pdf(uploaded_file)

# 7. Conteúdo Principal
if st.session_state.doc_text:
    tab1, tab2 = st.tabs(["📊 Relatório de Auditoria", "💬 Chat com o Documento"])

    with tab1:
        if st.button("🚀 Gerar Análise de Qualidade e Riscos"):
            with st.spinner("A IA está analisando cláusulas, riscos e conformidades..."):
                st.session_state.analysis_result = analyze_document(st.session_state.doc_text)

        if st.session_state.analysis_result:
            st.markdown(st.session_state.analysis_result)

    with tab2:
        st.subheader("Pergunte algo sobre este documento")
        user_question = st.text_input("Sua dúvida:")
        if user_question:
            with st.spinner("Buscando resposta..."):
                try:
                    chat_prompt = f"Com base neste documento: {st.session_state.doc_text[:10000]}\n\nResponda à pergunta: {user_question}"
                    chat_response = model.generate_content(chat_prompt)
                    st.write(chat_response.text)
                except Exception as e:
                    st.error(f"Erro no chat: {str(e)}")
else:
    st.info("👈 Para começar, faça o upload de um arquivo PDF no painel à esquerda.")