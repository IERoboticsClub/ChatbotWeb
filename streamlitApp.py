import streamlit as st

if "messages" not in st.session_state:  
    st.session_state.messages = []  

# Display chat history  
for message in st.session_state.messages:  
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])  

# User input  
if prompt := st.chat_input("Type your message..."):  
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})  
    with st.chat_message("user"):  
        st.markdown(prompt)  
