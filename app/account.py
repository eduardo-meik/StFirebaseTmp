#account.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Encapsulated Firebase Initialization
def initialize_firebase():
    if not firebase_admin._apps:
        cred = st.secrets("textkey")
        firebase_admin.initialize_app(cred)

def account():
    st.title('Welcome to Knowledge Base')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f(): 
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            st.session_state.signedout = True
            st.session_state.signout = True    
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if  not st.session_state["signedout"]:
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')

        col1, col2 = st.columns(2)  # Create two columns

        # In the first column, display the Login button
        with col1:
            if st.button('Login'):
                f() # Call the login function

        # In the second column, display the Signup button and associated logic
        with col2:
            if st.button('Sign up'):
                username = st.text_input("Enter  your unique username inside the signup button")
                if username:  # If user entered a username
                    user = auth.create_user(email=email, password=password, uid=username)
                    st.success('Account created successfully!')
                    st.markdown('Please Login using your email and password')
                    st.balloons()

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)

        



