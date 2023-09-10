#app.py
import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
from app.embeddings import display_embeddings
from app.chat import display_chat
from app.store import display_store
from app.qa import display_qa
from app.extract import display_extract
import requests

# Initialize Firebase SDK
def initialize_firebase():
    key_dict = json.loads(st.secrets["textkey"])
    creds = credentials.Certificate(key_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(creds)
# Define main app function
def main():
    initialize_firebase()
    
# Navigation bar Menu
selected = option_menu(
        menu_title=None, # menu title
        options=['Inicio', 'Embeddings','Chat','Q&A', 'Extract', 'Store'], # menu options
        icons=['house', 'boxes','chat-right-text', 'question-circle', 'layers', 'archive'], # menu icons
        menu_icon="cast", # menu icon
        default_index=0,  # default selected index
        orientation="horizontal" #sidebar or navigation bar
        )

if selected == "Inicio":
    st.title("Inicio")

elif selected == "Embeddings":
    st.title("Embeddings")
    display_embeddings()
    
elif selected == "Chat":
    st.title("Chat")
    display_chat()
    
elif selected == "Q&A":
    st.title("Questions & Answers")
    display_qa()

elif selected == "Extract":
    st.title("Extract")
    display_extract()
        
elif selected == "Store":
    st.title("Store")
    display_store()