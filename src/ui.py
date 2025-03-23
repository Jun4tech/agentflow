import streamlit as st
import time
import httpx
import json

st.title("Welcome to workflow assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello's How can I help you?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Assistant"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Make a stream request to the local server
        try:
            payload = {"message": prompt}
            headers = {"accept": "application/json", "Content-Type": "application/json"}
            with httpx.stream(
                "POST",
                "http://127.0.0.1:8000/api/stream?agent_name=search_agent",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                for chunk in response.iter_text():
                    data = json.loads(
                        chunk[5:]
                    )  # Remove "data: " prefix and parse JSON should be handled
                    if data["type"] == "web_search":
                        full_response += "Let me find information from the web...\n\n"
                    elif data["type"] == "web_result":
                        urls = [result["url"] for result in json.loads(data["content"])]
                        full_response += "I Found below sources for my reference: \n"
                        full_response += "\n".join(urls) + "\n\n"
                    else:
                        full_response += f"{data['content']} "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response)
        except Exception:
            response = "Sorry, I could not process your query at the moment. Please try again later."
            message_placeholder.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
