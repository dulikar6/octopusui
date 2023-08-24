import streamlit as st
import requests
from streamlit_app import session_id, file_name
from services.api_endpoints.api_calls import generate_excel_chat


def main():

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # Function for generating LLM response
    # def generate_response(prompt_input, session_id):
    #
    #
    #     headers = {
    #         'accept': 'application/json',
    #         'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    #     }
    #     params = {
    #         'input_message': prompt_input,
    #         'session_id': session_id,
    #     }
    #     response = requests.get('https://ocotopus.azurewebsites.net/chat_convo/', params=params, headers=headers)
    #     print(response.text)
    #     return response.text


    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_excel_chat(prompt, session_id, file_name)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
