import os
import time
import streamlit as st
import comet_llm
from openai import OpenAI

#used the medical chatbot AI advice list from an article on Medium, CometML and OpenAI (turbo-3.5) APIs but I keep getting 429 error code

st.title("AI-Powered Healthcare Chatbot")
st.write("Ask any medical question, our AI doctor is here to help!")

comet_llm.init(
    api_key=os.getenv("API_KEY"),  
    project="Doc_bot_openai"
)

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

advice_list = '''
# Medical Advice List

## General Health:
- Healthy Diet: Include a variety of fruits and vegetables in your diet.
- Regular Exercise: Aim for at least 30 minutes of moderate exercise most days of the week.
- Adequate Sleep: Ensure you get 7-9 hours of sleep per night for overall well-being.

## Common Ailments:
- Cold and Flu Remedies: Stay hydrated, get plenty of rest, and consider over-the-counter cold remedies.
- Headache Relief: Drink water, rest in a quiet room, and consider pain relievers.

## Emergency Situations:
- First Aid for Burns: Run cold water over the burn, cover with a clean cloth, and seek medical attention.
- CPR Guidelines: Call for help, start chest compressions, and follow emergency protocols.
'''

context_doctor = [
    {'role': 'system', 'content': f"""
    You are DoctorBot, an AI assistant providing medical advice.
    
    Be empathetic and informative in your responses.
    
    The Current Medical Advice List:
    ```{advice_list}```
    """}
]

if "messages" not in st.session_state:
    st.session_state.messages = []
    
def format_message(role, content):
    if role == "user":
        return f'<div style="background-color:#DCF8C6; padding:10px; border-radius:10px; max-width:80%;"><b>User:</b><br>{content}</div>'
    else:
        return f'<div style="background-color:#E1E1E1; padding:10px; border-radius:10px; max-width:80%;"><b>DoctorBot:</b><br>{content}</div>'


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask a health-related question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    context_doctor.append({'role': 'user', 'content': user_input})

    st.rerun()

    start_time = time.time()
    
    chat_completion = client.chat.completions.create(
        messages=context_doctor,
        model="gpt-3.5-turbo"
    )
    response = chat_completion.choices[0].message.content
    duration = time.time() - start_time

    with st.spinner("DoctorBot is thinking... 🤔"):
        response = get_openai_response(context_doctor)


    comet_llm.log_prompt(
        prompt=user_input,
        output=response,
        duration=duration,
        metadata={"context": context_doctor, "advice_list": advice_list}
    )

    st.session_state.messages.append({"role": "assistant", "content": response})
    context_doctor.append({'role': 'assistant', 'content': response})

    with st.chat_message("assistant"):
        st.write(response)
