import streamlit as st

from services import components
from services.api_endpoints.api_calls import load_file_names
from services.utils.page import page_group

import uuid

session_id = str(uuid.uuid4())

files = load_file_names()

file_name=None

def main():
    global file_name

    page = page_group("p")

    with st.sidebar:
        st.title("  insight.a❕")

        with st.expander("📃 FILES", True):

            files.append("ALL")

            selected_file = st.radio("Select a File:", files)

            for file in files:
                if selected_file == file:
                    if file_name == 'ALL':
                        file_name = None
                        st.write(f"Chatting with all the files")
                    else:
                        file_name = file
                        st.write(f"{file} is selected")


        with st.expander("🧩 APPS", True):
            page.item("Convo CHAT", components.convo_chat, default=True)
            page.item("PDF CHAT", components.pdf_chat_ui)
            page.item("Excel CHAT", components.excel_chat_ui)
            page.item("FILE UPLOAD", components.upload_file)

    page.show()

if __name__ == "__main__":
    st.set_page_config(page_title="insight.ai", page_icon="🔮", layout="wide")
    main()
