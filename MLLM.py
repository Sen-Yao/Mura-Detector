import base64
import requests
import cv2


def encode_image(image):
    image = cv2.resize(image, (1920, 1080))
    # Convert the image to PNG format
    _, buffer = cv2.imencode('.png', image)
    # Encode the image to base64
    return base64.b64encode(buffer).decode('utf-8')


def analyze_image(user_input, image, chat_history):
    api_key = "sk-Xxn1oSWs7aOiwuWU5c37733b68574256A5621726AcCa7cEa"

    # Getting the base64 string
    base64_image = encode_image(image)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    if chat_history:
        # Get the last element of chat_history
        last_entry = chat_history[-1]

        # Check if 'content' exists in the last entry and is a list
        if 'content' in last_entry and isinstance(last_entry['content'], list):
            # Iterate through the content list to find the image
            last_entry['content'] = [
                item for item in last_entry['content']
                if not (isinstance(item, dict) and item.get('type') == 'image_url')
            ]
    # Append new user input to chat history
    chat_history.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    })

    payload = {
        "model": "gpt-4o",
        "messages": chat_history,
    }

    print('对话中')
    response = requests.post("https://api.xeduapi.com/v1/chat/completions", headers=headers, json=payload)
    # Append assistant's response to chat history
    assistant_response = response.json()['choices'][0]['message']['content']

    chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    return assistant_response, chat_history
