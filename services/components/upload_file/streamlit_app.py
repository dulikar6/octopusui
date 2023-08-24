import streamlit as st
import requests


def upload_file_to_server(file, session_id=None, access_level_id=None):
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
    # session_id = st.text_input("Enter session ID")
    # access_level_id = st.text_input("Enter access level ID")

    if st.button("Upload"):
        if uploaded_file is not None:
            with st.spinner("File Uploading..."):
                response_text = upload_file_to_server(uploaded_file)
                st.write("FILE UPLOADED SUCCESSFULLY PLEASE PROCEED TO PDF OR EXCEL CHAT")
        else:
            st.warning("Please provide all required information.")


if __name__ == "__main__":
    st.set_page_config(page_title="File Upload Example", layout="wide")
    main()
