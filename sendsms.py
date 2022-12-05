import json
import requests


def send_sms(message: str, phone_number: str):
    '''
    Function that sends an sms text using a SMS sender API.
    Input : message : str , phone_number:str
    Output : Status of post-call
    '''
    request = requests.post(
        "https://textbelt.com/text",
        {
            "phone": phone_number,
            "message": message,
            "key": "textbelt_test",
        },
    )

    response = request.json()
    print(response)
