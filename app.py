from requests import get
import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets['AIzaSyDEuAJY-A4-aSY7YjjYsxPyFv-Hfmz6fi8'])

# Initialise Gemini model
gemini = genai.GenerativeModel('gemini-pro')

# function to fetch email
def get_email(sender, receiver, about, type, emojis, length):
    prompt = '''
    Write an email from {} to {}. The email is about {}. The email should be {} and {} characters long. {}
    '''.format(sender, receiver, about, type, length, "Use emojis in the email to make it attractive." if emojis else "Don't use emojis in the email.")
    
    response = gemini.generate_content(prompt)
    return response.text

# Begin with UI
st.set_page_config(
    page_title="Email Generator",
    page_icon=":email:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("Write emails like a pro")
st.write("Describe the type of email you want by filling in the following fields. Gemini will then generate an email for you.")

# Get user input
rec_col, sender_col = st.columns(2)

with rec_col:
    receiver = st.text_input("Who is the email for?")
    
with sender_col:
    sender = st.text_input("Who is the email from?")

len_col, email_type_col = st.columns(2)

with len_col:
    length = st.slider("How long should the email be?", min_value=50, max_value=500, value=200, step=50)

with email_type_col:
    email_type = st.selectbox("What type of email is it?", ["Formal", "Informal"])

about = st.text_area("What is the email about?")

use_emojis = st.toggle("Use emojis")

generate = st.button("Generate email")

# Generate email
if generate:
    with st.spinner("Generating email..."):
        try:
            if email_type and about and receiver and sender:
                email = get_email(sender, receiver, about, email_type.lower(), use_emojis, length)
                st.write(email)
            else:
                st.error("Please fill in all the fields.")
        except Exception as e:
            st.error("An error occurred. Please try again later.")
            st.error(e)