import time
import streamlit as st
from utils import cria_chain_conversa, PASTA_ARQUIVOS
import os

def sidebar():
    # Verifica se a sessão foi encerrada e redefine a chave da API
    if 'api_key' in st.session_state:
        api_key = st.text_input("Digite sua chave da API OpenAI:", value=st.session_state['api_key'], type="password")
    else:
        api_key = st.text_input("Digite sua chave da API OpenAI:", type="password")

    # Salvar a chave no estado da sessão
    if api_key:
        st.session_state['api_key'] = api_key

    uploaded_pdf = st.file_uploader(
        'Adicione seus arquivos PDF', type=['.pdf'], accept_multiple_files=True
    )

    if uploaded_pdf is not None:
        # Remove arquivos existentes antes de adicionar novos
        for arquivo in PASTA_ARQUIVOS.glob('*.pdf'):
            try:
                arquivo.unlink()
            except FileNotFoundError:
                st.error(f"Arquivo {arquivo.name} não encontrado")

        # Salva os novos PDFs
        for pdf in uploaded_pdf:
            with open(PASTA_ARQUIVOS / pdf.name, 'wb') as f:
                f.write(pdf.read())

    label_botao = 'Iniciar ChatBot'
    if 'chain' in st.session_state:
        label_botao = 'Atualizar ChatBot'

    if st.button(label_botao, use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob('*.pdf'))) == 0:
            st.error('Adicione arquivos no formato PDF para iniciar')
        elif 'api_key' not in st.session_state:
            st.error('Digite a chave da API para continuar')
        else:
            st.success('Iniciando ChatBot...')
            cria_chain_conversa()
            st.rerun()

    # Botão para encerrar a sessão
    if st.button("Encerrar Sessão", use_container_width=True):
        # Limpa a chave da API do estado da sessão
        if 'api_key' in st.session_state:
            del st.session_state['api_key']
        
        # Remove os arquivos PDF
        for arquivo in PASTA_ARQUIVOS.glob('*.pdf'):
            try:
                arquivo.unlink()
            except FileNotFoundError:
                st.error(f"Arquivo {arquivo.name} não encontrado")
        
        # Limpa o estado da sessão
        st.session_state.clear()
        
        # Exibe mensagem de sucesso
        st.success("Sessão encerrada com sucesso")

def chat_window():
    st.header('🤖 Bem-vindo ao chat com PDF', divider=True)

    if 'chain' not in st.session_state:
        return  # Não exibe mais nada

    chain = st.session_state['chain']
    memory = chain.memory
    mensagens = memory.load_memory_variables({})['chat_history']

    container = st.container()
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    nova_mensagem = st.chat_input('Converse com seu documento.....')
    if nova_mensagem:
        chat = container.chat_message('human')
        chat.markdown(nova_mensagem)

        chat = container.chat_message('ai')
        chat.markdown('Gerando Resposta')

        resposta = chain.invoke({'question': nova_mensagem})
        st.session_state['ultima_resposta'] = resposta
        st.rerun()

def main():
    with st.sidebar:
        sidebar()
    chat_window()

if __name__ == "__main__":
    main()
