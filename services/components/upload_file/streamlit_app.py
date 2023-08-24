import streamlit as st
import requests


def upload_file_to_server(file, session_id, access_level_id):
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    files = {
        'file': (file.name, file, 'application/pdf'),
        'session_id': (None, session_id),
        'access_level_id': (None, access_level_id),
    }

    response = requests.post('https://ocotopus.azurewebsites.net/file_uploader/', headers=headers, files=files)
    return response.text


def main():
    st.title("File Upload Example")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    session_id = st.text_input("Enter session ID")
    access_level_id = st.text_input("Enter access level ID")

    if st.button("Upload"):
        if uploaded_file is not None and session_id and access_level_id:
            response_text = upload_file_to_server(uploaded_file, session_id, access_level_id)
            st.write("Response:", response_text)
        else:
            st.warning("Please provide all required information.")


if __name__ == "__main__":
    st.set_page_config(page_title="File Upload Example", layout="wide")
    main()
