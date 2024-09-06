import requests

def thought_extractor(user_input):
    api_key = "sk-Xxn1oSWs7aOiwuWU5c37733b68574256A5621726AcCa7cEa"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    chat_history = [{
        "role": "system",
        "content":
            "You are a text extractor, and your task is to extract key strings from the input."
            "The input text may contain two different kinds of information for you to extract."
            "The first is a Tool with a number or the word \"finish,\" such as \"Tool 1,\" \"Tool 2,\" or \"finish.\""
            "The second, which is optional, is the parameter required by some Tools."
            "If parameters are mentioned in the text, you need to extract them as well."
            "For example: \"0.3, 0.4, 0.8, 0.9\""
            "You must extract this information and return it in brackets like {}."
            "For example: {Tool 1}{0.3, 0.4, 0.8, 0.9}"
    }, {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    }]

    # Append new user input to chat history

    payload = {
        "model": "gpt-4o-mini",
        "messages": chat_history,
    }

    print('对话中')
    response = requests.post("https://api.xeduapi.com/v1/chat/completions", headers=headers, json=payload)
    # Append assistant's response to chat history
    if 'choices' not in response.json():
        print(response.json(), '\n\n')
    assistant_response = response.json()['choices'][0]['message']['content']

    return assistant_response


