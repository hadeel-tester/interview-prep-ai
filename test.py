import streamlit as st
st.title("Hello, World!")
st.header("This is a header with a divider", divider="rainbow")
st.markdown("This is created using Streamlit, a powerful framework for building interactive web applications in Python.")
x = st.slider("Select an x value", 1, 10)
message_to_Chatgpt = st.text_input("Enter your message to ChatGPT here")