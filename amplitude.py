import os

import requests
import json
from aiogram.types import Message


async def send_amplitude_event(message: Message) -> None:
    amplitude_api_key = os.getenv('AMPLITUDE_API_KEY')
    amplitude_event_type = "Sign up"

    amplitude_data = {
        "api_key": amplitude_api_key,
        "events": [{
            "device_id": str(message.from_user.id),  # Используем user id в качестве device_id
            "event_type": amplitude_event_type
        }]
    }

    amplitude_headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    amplitude_response = requests.post('https://api2.amplitude.com/2/httpapi',
                                       headers=amplitude_headers, data=json.dumps(amplitude_data))

    if amplitude_response.status_code == 200:
        print("Amplitude Success:", amplitude_response.json())
    else:
        print("Amplitude Error:", amplitude_response.text)
