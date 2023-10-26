#main.py
import streamlit as st
import json
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
from app.embeddings import display_embeddings
from app.chat import display_chat
from app.store import display_store
from app.qrvcard import display_qr
from app.extract import display_extract
from app.account import account  # Importing the account module

# Initialize Firebase SDK
def initialize_firebase():
    key_dict = json.loads(st.secrets["textkey"])
    creds = credentials.Certificate(key_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(creds)

# Define main app function
def main():
    try:
        initialize_firebase()
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Check for authentication
    if not st.session_state.get("signedout", False):  # User not logged in
        account()  # This calls the account function which handles authentication
        return  # Ensures that the rest of the application doesn't run until the user is authenticated
    
    # Below this point, your main application code goes
    # Navigation bar Menu
    selected = option_menu(
        menu_title=None,  # menu title
        options=['Inicio', 'QR vCard', 'Store'],  # menu options
        icons=['house', 'layers', 'archive'],  # menu icons
        menu_icon="cast",  # menu icon
        default_index=0,  # default selected index
        orientation="horizontal"  # sidebar or navigation bar
    )

    if selected == "Inicio":
        st.title("Inicio")
    elif selected == "QR vCard":
        st.title("QR vCard")
        display_qr()
    elif selected == "Store":
        st.title("Store")
        display_store()

if __name__ == "__main__":
    main()
