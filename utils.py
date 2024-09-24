import os
from pathlib import Path
import streamlit as st
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI

from configs import *

PASTA_ARQUIVOS = Path(__file__).parent / "arquivos"

def importacao_documentos():
    documentos = []
    for arquivo in PASTA_ARQUIVOS.glob('*.pdf'):
        loader = PyPDFLoader(str(arquivo))
        documentos_arquivos = loader.load()
        documentos.extend(documentos_arquivos)
    return documentos

def split_de_documents(documentos):
    recurs_spliter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    documentos = recurs_spliter.split_documents(documentos)
    for i, doc in enumerate(documentos):
        doc.metadata['source'] = doc.metadata['source'].split('/')[-1]
        doc.metadata['doc_id'] = i
    return documentos

def cria_vector_store(documentos):
    embedding_model = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(
        documents=documentos, 
        embedding=embedding_model
    )
    return vector_store

def cria_chain_conversa():
    if 'api_key' not in st.session_state:
        raise ValueError("A chave da API não foi fornecida.")
    
    documentos = importacao_documentos()
    documentos = split_de_documents(documentos)
    vector_store = cria_vector_store(documentos)

    chat = ChatOpenAI(model_name=get_config('model_name'), openai_api_key=st.session_state['api_key'])
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key='chat_history',
        output_key='answer'
    )
    retriver = vector_store.as_retriever(
        search_type=get_config('retrieval_search_type'),
        search_args=get_config('retrieval_kwargs')
    )
    prompt_template = PromptTemplate.from_template(get_config('prompt'))
    
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriver,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': prompt_template}
    )

    st.session_state['chain'] = chat_chain
