#embedding.py
import pandas as pd
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings


@st.cache_data  # Modified the decorator
def create_embeddings(text):
    # Fetch the API key from st.secrets
    OPENAI_API_KEY = st.secrets["OpenAI"]["OPENAI_API_KEY"]


    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    texts = text_splitter.create_documents([text])

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    embeddings_query_result = []

    for i, doc in enumerate(texts):
        query_result = embeddings.embed_query(doc.page_content)
        embeddings_query_result.extend(query_result)

    embeddings_df = pd.DataFrame(embeddings_query_result, columns=["embedded_values"])

    return texts, embeddings, embeddings_df


def display_embeddings():
    st.write("Upload a text file for embedding...")
    
    # Upload a file to test
    uploaded_file = st.file_uploader("Choose a file", type=['txt'])
    
    if uploaded_file:
        text_content = uploaded_file.read().decode("utf-8")
        texts, embeddings, embeddings_df = create_embeddings(text_content)
        
        st.write(embeddings_df)  # Displaying the embeddings dataframe

