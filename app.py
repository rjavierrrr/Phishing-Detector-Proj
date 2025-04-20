from PIL import Image
import pytesseract
from phishing_detector import analyze_email_with_gpt

import streamlit as st

st.set_page_config(page_title="Phishing Detection Tool", layout="centered")

st.title("Phishing Detection Using OpenAI")
st.write("You can enter the email content manually or upload an image of the email to analyze it.")

input_type = st.radio("Select input type:", ("Text", "Image"))

email_text = ""

if input_type == "Text":
    email_text = st.text_area("Email content:", height=300)

elif input_type == "Image":
    uploaded_file = st.file_uploader("Upload an image of the email (JPEG, PNG):", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image", use_container_width=True)
        email_text = pytesseract.image_to_string(image)
        st.text_area("Extracted text (via OCR):", email_text, height=200)

if st.button("Analyze"):
    if email_text.strip():
        with st.spinner("Analyzing with GPT..."):
            result = analyze_email_with_gpt(email_text)
        st.success("Analysis result:")
        st.write(result)
    else:
        st.warning("Please enter text or upload a valid image before analyzing.")
