# 📄 DocIntelligence AI

Aplicação web desenvolvida em Python e Streamlit para análise automatizada de documentos corporativos, contratos e minutas utilizando a API do Google Gemini (`google-genai`).

## 🚀 Funcionalidades
- **Extração de Texto:** Leitura rápida de ficheiros PDF via `pypdf`.
- **Relatório de Auditoria Instantâneo:** Geração em tempo real (Streaming) de resumo executivo, fatos/dados principais e análise de riscos/conformidades.
- **Chat Interativo:** Canal contextual de perguntas e respostas com base no documento carregado.

## 🛠️ Tecnologias Utilizadas
- Python 3.13+
- Streamlit
- Google GenAI SDK (`google-genai`)
- PyPDF & python-dotenv

## ⚙️ Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/amandafilippi/doc-intelligence-ai.git
   cd doc-intelligence-ai

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

4. **Configure a variável de ambiente:**
   Crie um ficheiro `.env` na raiz do projeto e adicione a sua chave:
   ```env
   GEMINI_API_KEY=sua_chave_aqui

5. **Inicie a aplicação:**
   ```bash
   streamlit run app.py
´´´
