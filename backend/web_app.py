
import streamlit as st

from backend.rag import generate_answer


st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.write("Ask questions about your uploaded documents.")


# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Accept a new question
question = st.chat_input("Type your question here...")


if question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    # Generate chatbot response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = generate_answer(question)

            st.write(answer)

    # Save chatbot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
