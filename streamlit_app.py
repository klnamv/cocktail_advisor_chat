import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"


st.markdown(
    "<h1 position: fixed; top: 0; width: 100%;'>Cocktail Q&A Chatbot 🍸</h1>",
    unsafe_allow_html=True,
)
st.markdown("Ask me anything about cocktails, and I'll provide an answer")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        text, image_url = message["content"].rsplit("\n", 1)
        formatted_text = f"""
                <div style="font-size: 16px; line-height: 1.6;">
                    {text.replace("•", "").replace("-", "")}
                </div>
                """
        st.markdown(formatted_text, unsafe_allow_html=True)
        st.image(image_url, width=300)

user_input = st.chat_input("Type your question about cocktails...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = requests.post(API_URL, json={"question": user_input})
        if response.status_code == 200:
            answer = response.json().get("answer", "No response available.")
        else:
            answer = "Error: Unable to fetch response from the server."
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)