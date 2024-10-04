# authentication.py
from dotenv import load_dotenv
import requests
import os
import streamlit as st


load_dotenv()

# Set your Auth0 credentials
AUTH0_DOMAIN = "dev-vignesh123.us.auth0.com"  # Your Auth0 domain
CLIENT_ID = "CBFDvbwEcN77VdMojIv6wnQCDFlFhIGS"          # Your Auth0 client ID
CLIENT_SECRET = "gEkZLOclTieJ9x8yu5GG2aUFYxbtNSa_Zc3kFS9tPzNzx_SzmKi-IU3kBXarh8Wy" # Your Auth0 client secret
REDIRECT_URI = "http://localhost:8501/callback"    # Your callback URL

def get_login_url():
    return (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&"
        f"redirect_uri={REDIRECT_URI}&scope=openid profile email"
    )



def handle_login(code):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {'Content-Type': 'application/json'}
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Login failed! Please try again.")
        return None

def main():
    st.sidebar.markdown(f"[Login with Auth0]({get_login_url()})")
    
    # Handle the redirect from Auth0
    code = st.query_params.get("code")
    if code:
        tokens = handle_login(code[0])
        if tokens:
            st.session_state['id_token'] = tokens.get('id_token')
            st.sidebar.success("Logged in successfully!")
