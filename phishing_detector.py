import pandas as pd
import streamlit as st
from openai import OpenAI
import random

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def build_fewshot_prompt(email_text: str) -> str:
    try:
        df = pd.read_csv("Phishing_Email.csv")

        
        df = df[df["Email Text"].notna()]
        df = df[df["Email Text"].str.lower() != "empty"]

        
        df["Label"] = df["Email Type"].apply(
            lambda x: "Phishing" if "phishing" in x.lower() else "Legitimate"
        )

        
        phishing_examples = df[df["Label"] == "Phishing"].sample(3, random_state=42)
        legit_examples = df[df["Label"] == "Legitimate"].sample(3, random_state=42)

        prompt = (
            "You are a cybersecurity assistant. Below are examples of emails and their classification.\n"
            "Classify the final email using the same criteria.\n\n"
        )

        for _, row in pd.concat([phishing_examples, legit_examples]).iterrows():
            prompt += f'Email: "{row["Email Text"].strip()}"\nLabel: {row["Label"]}\n\n'

        prompt += (
            f'\nNow analyze this email:\n"{email_text}"\n'
            "Explain briefly why it's considered phishing or legitimate. Return the final label as 'Phishing' or 'Legitimate'."
                )
        return prompt

    except Exception as e:
        return f"Email:\n{email_text}"

def analyze_email_with_gpt(email_text: str) -> str:
    prompt = build_fewshot_prompt(email_text)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content
