import streamlit as st
from streamlit_app import session_id, file_name
from services.api_endpoints.api_calls import generate_pdf_chat
import time

def main():

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    # User-provided prompt
    if prompt := st.chat_input(disabled=not (True)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        # with st.chat_message("assistant"):
        #     with st.spinner("Thinking..."):
        #         response = generate_pdf_chat(prompt, session_id, file_name)
        #         st.write(response)
        # message = {"role": "assistant", "content": response}
        # st.session_state.messages.append(message)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                message_placeholder = st.empty()
                full_response = ""
                assistant_response, source_data_list = generate_pdf_chat(prompt, session_id, file_name)
                # Simulate stream of response with milliseconds delay
                for chunk in assistant_response.split():
                    full_response += chunk + " "
                    time.sleep(0.06)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

                # enh_expander = st.expander("Citations", expanded=False)
                # with enh_expander:
                #     st.write("  insight.a❕")
                # Combine content from all items in the list
                combined_content = "\n\n".join(item['page_content'] for item in source_data_list)
                # Create a single expander with the combined content
                with st.expander("Source Citation"):
                    st.markdown(
                        f'<div style="overflow-y: scroll; max-height: 300px;">{combined_content}</div>',
                        unsafe_allow_html=True
                    )

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()
