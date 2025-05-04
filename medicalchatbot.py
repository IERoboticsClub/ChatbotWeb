import os
import time
import streamlit as st
import json
import comet_llm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_KEY")


#used the medical chatbot AI advice list from an article on Medium and OpenAI's (turbo-3.5) API

st.title("AI-Powered Healthcare Chatbot")
st.write("Ask any medical question, our AI doctor is here to help!")


client = OpenAI(api_key=OPENAI_API_KEY)

data_about_cancer = 'data/cleaned_data.jsonl'
if os.path.exists(data_about_cancer):
    with open(data_about_cancer, "r", encoding="utf-8") as f:
        cancer_data = [json.loads(line) for line in f if line.strip()]
else:
    cancer_data = []

response = client.files.create(
    file=open(data_about_cancer), 
    purpose="fine-tune"
)

training_file_id = response['id']

fine_tuned_response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    model= "gpt-3.5-turbo",
    n_epochs = 10,
    batch_size = 5
)

fine_tuned_model = fine_tuned_response.model

if "messages" not in st.session_state:
    st.session_state.messages = []
    


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask a health-related question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("The chatbot is generating a response, this might take a while..."):
        start_time = time.time()
        
        chat_completion = client.chat.completions.create(
            model=fine_tuned_model,
            messages=st.session_state.messages
        )
        
        response = chat_completion.choices[0].message.content
        duration = time.time() - start_time

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)
