from requests import get
import streamlit as st
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure Gemini
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

# Initialise Gemini model
gemini = genai.GenerativeModel('gemini-pro')

# Function to fetch email
def get_email(sender, receiver, about, type, emojis, length):
    prompt = '''
    Write an email from {} to {}. The email is about {}. The email should be {} and {} characters long. {}
    '''.format(sender, receiver, about, type, length, "Use emojis in the email to make it attractive." if emojis else "Don't use emojis in the email.")
    
    response = gemini.generate_content(prompt)
    return response.text

# Function to send email using SMTP
def send_email(sender_email, sender_password, receiver_email, subject, email_body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # For Gmail
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return str(e)

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
    receiver = st.text_input("Who is the email for? (Receiver's Email Address)")
    
with sender_col:
    sender = st.text_input("Who is the email from?")

len_col, email_type_col = st.columns(2)

with len_col:
    length = st.slider("How long should the email be?", min_value=50, max_value=500, value=200, step=50)

with email_type_col:
    email_type = st.selectbox("What type of email is it?", ["Formal", "Informal"])

about = st.text_area("What is the email about?")
use_emojis = st.checkbox("Use emojis")

# Email sending fields
st.write("Provide your email credentials to send the generated email.")
sender_email = st.text_input("Your Email Address")
sender_password = st.text_input("Your Email Password", type="password")
subject = st.text_input("Email Subject")

generate = st.button("Generate and Send Email")

# Generate and send email
if generate:
    with st.spinner("Generating email..."):
        try:
            if email_type and about and receiver and sender and sender_email and sender_password and subject:
                email_body = get_email(sender, receiver, about, email_type.lower(), use_emojis, length)
                st.write("Generated Email:")
                st.write(email_body)
                st.write("Sending email...")
                result = send_email(sender_email, sender_password, receiver, subject, email_body)
                st.success(result)
            else:
                st.error("Please fill in all the fields.")
        except Exception as e:
            st.error("An error occurred. Please try again later.")
            st.error(e)
