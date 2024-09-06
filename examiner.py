import requests
from MLLM import encode_image


def ROI_examiner(bounding_box_parameter, image):
    api_key = "sk-Xxn1oSWs7aOiwuWU5c37733b68574256A5621726AcCa7cEa"
    base64_image = encode_image(image)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    chat_history = [{
        "role": "system",
        "content":
            "You are an image bounding box examiner. You will be provided with an image containing a white smartphone screen on a black background, "
            "and the corresponding relative coordinate values of the bounding box"
            "x1, y1 represent the relative coordinate values of the input's top-left. x=0 means the leftest side, and x=1 means the rightest side"
            "x2, y2 represent the relative coordinate values of the input's bottom-right.  y=0 means the top side, and x=1 means the bottom side"
            "The user will have marked a red bounding box, attempting to outline the potential smartphone screen."
            "However, this bounding box may not be accurate. You should analyze the current bounding box in relation to the actual smartphone screen in the image."
            "Based on your analysis, provide advice on how to adjust the bounding box."
            "When you give suggestion, you should explain clearly about the reason why you do these adjustments"
            "Note: Exercise caution to avoid inadvertently cutting off critical information when making adjustments."
    }, {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "This is the value:" + str(bounding_box_parameter) + "Can you see the bounding box and scaler in the image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
    }]

    payload = {
        "model": "gpt-4o",
        "messages": chat_history,
    }

    response = requests.post("https://api.xeduapi.com/v1/chat/completions", headers=headers, json=payload)
    print("examiner.py", response.json())
    # Append assistant's response to chat history
    assistant_response = response.json()['choices'][0]['message']['content']

    print("ROI Examiner's suggestion:", assistant_response)
    return assistant_response
