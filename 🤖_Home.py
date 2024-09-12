
import time
import streamlit as st
from utils import cria_chain_conversa, PASTA_ARQUIVOS

def sidebar():
    uploaded_pdf = st.file_uploader(
        'Adicione seus arquivos PDF', 
        type=['.pdf'], 
        accept_multiple_files=True
        )
    
    if not uploaded_pdf is None:
        for arquivo in PASTA_ARQUIVOS.glob('*.pdf'):
            arquivo.unlink()
        for pdf in uploaded_pdf:
            with open (PASTA_ARQUIVOS / pdf.name, 'wb') as f:
                f.write(pdf.read())
    


    label_botao = 'Incializar ChatBot'
    if 'chain' in st.session_state:
        label_botao = 'Atualizar ChatBot'        

    if st.button(label_botao, use_container_width=True):
        if len(list(PASTA_ARQUIVOS.glob('*.pdf'))) == 0:
                st.error('Adicione arquivos no formato PDF para iniciar')
        else:
            st.success('Iniciando ChatBot...')
            cria_chain_conversa()
            st.rerun()

    
def chat_window():
    st.header('🤖 Bem vindo ao chat com PDF', divider=True)

    if not 'chain' in st.session_state:
        st.error('Faça upload de PDFs para iniciar')
        st.stop()


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

