from services import components
from services.api_endpoints.api_calls import load_file_names, delete_files
from services.utils.page import page_group

import json
import streamlit as st
from streamlit_lottie import st_lottie


import uuid

session_id = str(uuid.uuid4())

files = load_file_names()

def main():


    page = page_group("p")

    with st.sidebar:

        path = "services/utils/lottie_jsons/animation_lloli41t.json"
        with open(path, "r") as file:
            url = json.load(file)

        st.markdown('<link rel="stylesheet" type="text/css" href="services/utils/css_files/styles.css">', unsafe_allow_html=True)

        st_lottie(url,
                  reverse=True,
                  height=200,
                  width=300,
                  speed=1,
                  loop=True,
                  quality='high',
                  key='Car'
                  )

        coll1, coll2, coll3 = st.columns(3)
        coll2.title("INSIGHT.A❕")

        st.title("")

        col1, col2 = st.columns(2)

        if col1.button("Delete All Files"):
            delete_files()
            st.radio("Select a File:", [])

        if col2.button("Clear Messages"):
            st.session_state.messages.clear()
            st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

        with st.expander("🧩 APPS", True):
            page.item("Convo CHAT", components.convo_chat, default=True)
            page.item("PDF CHAT", components.pdf_chat_ui)
            page.item("Excel CHAT", components.excel_chat_ui)
            page.item("FILE UPLOAD", components.upload_file)
            page.item("CAR EVALUATION", components.car_eval)


        with st.expander("📃 FILES", False):
            files.append("ALL")
            selected_file = st.radio("Select a File:", files)

            for file in files:
                if selected_file == file:
                    if file == 'ALL':
                        file_name = None
                        st.write(f"Chatting with all the files")
                    else:
                        st.session_state.file_name = file
                        st.write(f"{file} is selected")

    page.show()

if __name__ == "__main__":
    st.set_page_config(page_title="insight.ai", page_icon="🔮", layout="wide")
    main()
