import streamlit as st

st.title("AI-Powered Healthcare Chatbot")
st.write("Ask any medical related question, our AI doctor is here to help!")

if "messages" not in st.session_state:  
    st.session_state.messages = []  

for message in st.session_state.messages:  
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])  

if prompt := st.chat_input("Type your message..."):  
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.markdown(prompt)  
