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
def send_email(summary, email, sender_email, password):
    # Get the current date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Email subject
    subject = f"Meeting Summary - {current_datetime}"
    
    # Email header and footer
    header = "Dear Team,\n\n"
    footer = "\n\nRegards,\nSupport Team\nClubitsSolutions\n**This mail sent by Text to Summary app**"
    
    # Complete message
    message = header + summary + footer

    # Create a MIMEText object to represent the message
    msg = MIMEText(message)

    # Set the sender, recipient, and subject fields
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)  # Login to the email server
            server.sendmail(sender_email, email, msg.as_string())  # Send the email
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
summary = "This is a summary of the meeting."
email = "recipient@example.com"  # Replace with recipient's email
sender_email = input("Enter your email: ")  # Prompt the user for their email
password = input("Enter your email password: ")  # Prompt the user for their email password

send_email(summary, email, sender_email, password)
