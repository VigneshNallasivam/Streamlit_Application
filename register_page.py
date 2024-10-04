import streamlit as st

def register_page():
    # Load CSS from external file
    def load_css(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load your CSS file
    load_css('reg_style.css')  # Ensure the path is correct

    # Navigation links
    st.markdown(f'''
        <div class="topnav">
            <a href="https://www.google.com/">Home</a>
            <a href="https://www.youtube.com/">YouTube</a>
            <a href="#">Contact</a>
            <a href="#">About</a>
        </div>
    ''', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        image_path = "./images/search-engine.png"
        st.image(image_path, width=50)
        
    with col2:
        st.markdown('''<h1 class="title">APPLICATION FORM</h1>''', unsafe_allow_html=True)

    # Input fields for registration
    name = st.text_input("Name : ")
    gender_options = ['Male', 'Female']
    gender = st.selectbox("Gender:", gender_options)
    age = st.text_input("Age : ")
    district_options = ['Erode', 'Karur', 'Trichy', 'Salem', 'Tanjore', 'Chennai', 'Ooty', 'Namakkal', 'Tirunelveli', 'Kancheepuram']
    district = st.selectbox("District :", district_options)
    state_options = ['Tamil Nadu', 'Kerala', 'Andhra Pradesh', 'Karnataka', 'Telangana', 'Arunachal Pradesh', 'Himachal Pradesh', 'Madhya Pradesh', 'Maharashtra', 'Gujarat']
    state = st.selectbox("State :", state_options)
    mobile = st.text_input("Mobile : ")
    address = st.text_area("Address : ")

    # Submit and Cancel buttons
    st.markdown("""
        <div style="display: flex; margin-top: 20px;">
            <button class="cancel_button">Cancel</button>
            <button class="submit_button">Submit</button>
        </div>
    """, unsafe_allow_html=True)
