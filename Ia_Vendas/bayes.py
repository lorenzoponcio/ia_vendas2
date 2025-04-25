# IMPORTAR AS BIBLIOTECAS
import streamlit as st
import fitz
import requests

# CHAVE DA SUA API DA GROQ
GROQ_API_KEY = "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"

# Função para extrair texto dos arquivos PDF
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        with fitz.open(stream=pdf.read(), filetype="pdf") as doc: 
            for page in doc:
                text += page.get_text("text") 
    return text

# Função para perguntar à IA da Groq
def ask_groq(question, context, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "Você é um assistente de vendas que responde com base em um catálogo de computadores."},
            {"role": "user", "content": f"Catálogo de produtos:\n{context}"},
            {"role": "user", "content": question}
        ],
        "temperature": 0.7
    }



    response = requests.post(url, headers=headers, json=data)

    # Tenta converter a resposta para JSON
    try:
        result = response.json()
    except:
        return "Erro: não foi possível interpretar a resposta da IA."

    # Verifica se retornou erro
    if "error" in result:
        return f"Erro da API: {result['error'].get('message', 'Mensagem desconhecida')}"

    # Verifica se veio a resposta correta
    try:
        return result["choices"][0]["message"]["content"]
    except KeyError:
        return "Erro: resposta inesperada da IA. Verifique se a chave da API está correta ou se o modelo está disponível."


    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    return result["choices"][0]["message"]["content"]

# INTERFACE DO APP
def main():
    st.title("Assistente Inteligente de Vendas de Computadores")

    with st.sidebar:
        st.header("Upload do Catálogo")
        uploader = st.file_uploader("Adicione o catálogo em PDF", type="pdf", accept_multiple_files=True)

    if uploader:
        text = extract_files(uploader)
        st.session_state["document-text"] = text
        st.success("Catálogo carregado com sucesso!")

    if "document-text" in st.session_state:
        user_input = st.text_input("Faça uma pergunta sobre os computadores")
        if user_input:
            with st.spinner("Consultando a IA..."):
                response = ask_groq(user_input, st.session_state["document-text"], GROQ_API_KEY)
                st.markdown("### Resposta da IA:")
                st.write(response)

if __name__ == "__main__":
    main()
