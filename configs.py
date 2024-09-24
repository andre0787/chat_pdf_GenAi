import streamlit as st

MODEL_NAME = "gpt-4o-mini"
RETRIEVEL_SEARCH_TYOE = 'mmr'
RETRIEVEL_KWARGS = {'k': 3, "fetch_k": 20}
PROMPT = ''' Você é um Chatbot amigável que auxilia o usuário na interpretação de documentos que lhe são fornecidos.
No contexto fornecido estão informações dos documentos do usuário. Utilize o contexto para responder as perguntas do usuário.
Se você não sabe a resposta, diga apenas que não sabe e não tente inventar a resposta.

Contexto:
{context}

Conversa atual:
{chat_history}

Human:? {question}:
AI: '''

def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]

    if config_name.lower() == 'model_name':
        return MODEL_NAME
    
    if config_name.lower() == 'retrieval_search_type':
        return RETRIEVEL_SEARCH_TYOE

    if config_name.lower() == 'retrieval_kwargs':
        return RETRIEVEL_KWARGS

    if config_name.lower() == 'prompt':
        return PROMPT
