import streamlit as st
from langchain.prompts import PromptTemplate

from configs import get_config

def debug_page():
    st.header('Pagina de bebug', divider=True)
    prompt_template = get_config('prompt')
    prompt_template = PromptTemplate.from_template(prompt_template)
    
    
    if not 'ultima_resposta' in st.session_state:
        st.error('Realize uma pergunta para o modelo e visuealize o debug')
        st.stop()

    
    
    ultima_resposta = st.session_state['ultima_resposta']
    
    contexto_docs = ultima_resposta['source_documents']
    
    contexto_list = [doc.page_content for doc in contexto_docs]
    
    contexto_str = '\n\n'.join (contexto_list)
    
    
    chain = st.session_state['chain']
    memory = chain.memory
    chat_history = memory.buffer_as_str


    with st.container(border=True):
        prompt = prompt_template.format(
            chat_history = chat_history,
            question = '',
            answer = ultima_resposta['answer'],
            context = contexto_str
            
        )
        st.code(prompt)

    

debug_page()