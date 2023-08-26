import json
import re

import pandas as pd
import requests


def generate_conversation_chat(prompt_input, session_id):
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }
    params = {
        'input_message': prompt_input,
        'session_id': session_id,
    }
    response = requests.get('https://ocotopus.azurewebsites.net/chat_convo/', params=params, headers=headers)
    print(response)
    return response.text

def generate_pdf_chat(question, session_id, file_name, follow_up=False):

    print(f'{question} -- {session_id} -- {file_name}')

    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    params = {
        'question': question,
        'session_id': session_id,
        'file_name': file_name,
        'follow_up': follow_up
    }

    response = requests.get('https://ocotopus.azurewebsites.net/chat_pdf/', params=params, headers=headers)
    response_data = json.loads(response.text)
    source_documents = process_source_documents(response_data.get('source_documents'))
    if response_data.get('question_suggestions', None):
        process_question_list = process_questions(response_data.get('question_suggestions'))
    else:
        process_question_list = []
    return response_data.get('result'), source_documents, process_question_list

def generate_excel_chat(question, session_id, file_name):
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    params = {
        'question': question,
        'session_id': session_id,
        'file_name': file_name,
    }

    response = requests.get('https://ocotopus.azurewebsites.net/chat_excel/', params=params, headers=headers)
    response_data = response.text
    print(type(response_data))
    try:
        data = json.loads(response_data)
        return data.get('answer'), data.get('log')
    except:
        return "Can You be more specific please", "Sorry couldn't find an answer"

def load_excel_df(file_name):
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'd7lrds7UaL0BQSiUS2dPcFAXGKW5XHW35twz3IHacEAWtwoMm81qlMDxN9Pz0fD6',
    }

    params = {
        'file_name': file_name,
    }

    response = requests.get('https://ocotopus.azurewebsites.net/load_excels/', params=params, headers=headers)

    df = pd.DataFrame(json.loads(response.text))

    return df

def load_file_names():
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    response = requests.get('https://ocotopus.azurewebsites.net/file_detials/', headers=headers)

    response_data = json.loads(response.text)

    return [entry["file_name"] for entry in response_data]


def upload_files():
    headers = {
        'accept': 'application/json',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    files = {
        'file': open('FORM 18 - DON RANASINGHE DULIKA LAVANYA.pdf;type=application/pdf', 'rb'),
        'session_id': (None, 'as'),
        'access_level_id': (None, 'as'),
    }

    response = requests.post('https://ocotopus.azurewebsites.net/file_uploader/', headers=headers, files=files)
    return response.text

def delete_files():
    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'rbIwEMR0YzrIkFbUVoE1rH93qGMn3y4njaQyAPSEgoeswtKiTIAH9P3mTCAkprBo',
    }

    requests.get('http://127.0.0.1:8000/delete_files/', headers=headers)


def process_source_documents(data):
    data_set = []
    for page in data:
        source = {}
        source['page_content'] = page[0][1]
        source['file_name'] = page[1][1]['source']
        data_set.append(source)
    return data_set

def process_questions(data):
    print(data)
    lines = data.split("\n")
    lines = [line.strip() for line in lines if line.strip() != ""]

    # Extract the questions from the list
    questions = []
    for line in lines:
        if re.match(r"^\d+\.\s", line):
            questions.append(line[3:])  # Remove the numbering from the question
        elif questions:
            questions[-1] += " " + line  # Append continuation lines to the last question

    return questions
