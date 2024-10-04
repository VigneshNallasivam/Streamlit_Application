from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Home", layout="wide")

def home_page():
    def load_css(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    load_css('home_style.css') 
    # Set the image path
    image_path = "./images/tech_3.jpg"

    # Custom CSS for styling
    st.markdown(
        f"""
        <style>
        .background {{
            background-image: url({st.image({image_path})});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;  /* Change text color to white for better visibility */
            text-align: center;  /* Center text */
        }}
        
         </style>""",
        unsafe_allow_html=True)
    # Main content
    st.markdown(
        f"""
        <div class="background"> 
          <div class="sign">
            <a href="">Sign in</a>
            <a href="">Sign up</a>
          </div>
          <h1 class="title">Helpdesk</h1>
          <p class="subtitle">"Your Questions, Our Solutions"</p>
        </div>""",unsafe_allow_html=True
    )
   
    
    
def sidebar():
    def load_css(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    load_css('main.css') 
        
    st.sidebar.image("./images/ticket_3.png",width=80)

    st.sidebar.markdown('<p class="nav_title">NAVIGATION</p>', unsafe_allow_html=True)
    

    if st.sidebar.button("Home",key="home_button"):
        home_page()

    if st.sidebar.button("Register",key="register_button"):
        from register_page import register_page
        register_page()
    
    if st.sidebar.button("Tickets",key="issues_button"):
        from jira_connection import issue_fun
        issue_fun()

    if st.sidebar.button("Sign-in", key="signin_button"):
        if "id_token" in st.session_state:
            st.sidebar.success("You are already logged in!")
        else:
            # Redirect to Auth0 login page
            from authentication import get_login_url
            login_url = get_login_url()
            st.markdown(f'<meta http-equiv="refresh" content="0; url={login_url}">', unsafe_allow_html=True)
            
    if st.sidebar.button("Sign-out", key="signout_button"):
        if "id_token" in st.session_state:
            # Redirect to Auth0 logout URL
            from authentication import get_logout_url
            logout_url = get_logout_url()
            st.markdown(f'<meta http-equiv="refresh" content="0; url={logout_url}">', unsafe_allow_html=True)
            del st.session_state['id_token']  # Clear the session token
            st.sidebar.success("You have been logged out.")
        else:
            st.sidebar.warning("You are not logged in.")
            
    if st.sidebar.button("StreamGpt",key="gpt_button"):
        from chatbot import chat_func
        chat_func()
        
    if st.sidebar.button("logs",key="log_button"):
        from log_watcher_with_bell import fetch_new_error_logs
        fetch_new_error_logs()

        
        

def main():
    sidebar()

if __name__ == "__main__":
       main()