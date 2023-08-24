import json

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
    print(response.text)
    return response.text

def generate_pdf_chat(question, session_id, file_name):

    print(f'{question} -- {session_id} -- {file_name}')
    file_name = 'dulika_ranasinghe_cv.pdf'

    headers = {
        'accept': 'application/json',
        'X-CSRFToken': 'OrJ1S6ddplBQrTbrcfxIOUfRE0oSixyFGNU9ImNtrebb4xhjGlljX1irLphml5fI',
    }

    params = {
        'question': question,
        'session_id': session_id,
        'file_name': file_name,
    }

    response = requests.get('https://ocotopus.azurewebsites.net/chat_pdf/', params=params, headers=headers)
    response_data = json.loads(response.text)
    return response_data.get('result')

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
    response_data = json.loads(response.text)
    return response_data.get('result')

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
