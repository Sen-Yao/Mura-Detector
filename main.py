import cv2
from MLLM import analyze_image
from utils import extract_substrings
from extractor import thought_extractor
from examiner import ROI_examiner
import toolkit_function

image_path = "test.bmp"  # Replace with your image path
image = cv2.imread(image_path)

task_finish = False
counter = 0
chat_history = [
    {
        "role": "system",
        "content":
            "Your final goal is to locate all the defects in the given image of the smartphone"
            "and then represent the normalized coordinates of the identified regions."
            "Before achieving this final goal,"
            "you need to break it down into subtasks and solve them step by step."
            "In each step,"
            "you can call a tool from the predefined tool list to address the corresponding subtask."
            "For example, you may need to find the ROI of the screen."
            "Each tool has a description of its purpose and usage,"
            "and you can use the following tools"
            "while explaining why you believe it's the right time to use a particular tool."
            "These are the tools I provide:"
            "Tool 1: Name: Image Split,"
            "Description: Crop the image"
            "based on the relative coordinate values of the input's top-left and bottom-right corners."
            "Note that it's better to crop too loosely than to crop too much and risk losing information."
            "x1, y1 represent the relative coordinate values of the input's top-left"
            "x2, y2 represent the relative coordinate values of the input's bottom-right"
            "Example Call: \"I'll use {Tool 1} with coordinate values {0.1, 0.2, 0.8, 0.9}\""
            "Note: Exercise caution when using this tool to avoid inadvertently cutting off critical information."
            "If you're unsure about the relationship between the coordinate values and the corresponding bounding box, it's advisable to use Tool 3 before proceeding with this tool."
            "Before calling this tool, you should use tool 4 to exam your current bounding box of the screen edge"
            "Tool 2: Name: Distance Ruler,"
            "Description: Overlay a distance ruler for you to ensure the relative distance in the image. It is wise to use this tool before using Tool 1 for better accuracy."
            "Example Call: \"I'll use {Tool 2}\""
            "Tool 3: Name: Bounding Box,"
            "Description: Overlay a Bounding Box for you to mark the potential ROI of the screen, or mark the defects you found. It is wise to use Tool 2 before using tools that need relative coordinate values for better accuracy."
            "x1, y1 represent the relative coordinate values of the input's top-left"
            "x2, y2 represent the relative coordinate values of the input's bottom-right"
            "Example Call: \"I'll use {Tool 3} with coordinate values {0.1, 0.2, 0.8, 0.9}\""
            "You must call Tool 2 before you call this tool."
            "Strictly examine the value of parameters you choose"
            "Note: Exercise caution when using this tool to avoid inadvertently cutting off critical information."
            "Tool 4: Name: ROI Examiner"
            "Description: Examine your bounding box for the screen and provide some advice on how to adjust the bounding box."
            "You should call Tool 4 every time after you call Tool 3."
            "You can call Tool 3 to draw a better bounding box for the screen after you get advice from Tool 4."
            "Example Call: \"I'll use {Tool 4}\""
            "That's all the tools I've developed for you. You can ONLY call one tool in each response, but during the whole process, you can call the same Tool in different responses multiple times."
            "If you believe the final goal has been achieved, or you don't know what to do, you can explain what you're thinking and say {finish} with brackets."
            "The downstream function will extract your function call request based on the use of curly brackets {}."
            "During your process, don't ask me what to do next; just try to locate all the defects or abnormalities in the image."
            "Note that the screen you receive is not a perfect rectangle; it may have indentations (for placing the front camera, etc.)."

    }
]
response, chat_history = analyze_image('Find the bright smart phone screen in the image.', image, chat_history)

print("Initial response:", response)
thought = thought_extractor(response)
print("Extracting")
thought = extract_substrings(thought)
print("Initial thought:", thought)
user_input = ""
bounding_box_image = image.copy()
bounding_box_parameter = 0
while not task_finish and counter < 20:
    counter += 1
    if "finish" in thought:
        task_finish = True
        break
    if "Tool 1" in thought:
        image = toolkit_function.crop_image(image, thought[1])
        cv2.imwrite(f'log/{counter}cropped_image.jpg', image)
        user_input = "This is the cropped image. If you have any thought of the process, please let me know to help with you, What to do next?"
        response, chat_history = analyze_image(user_input, image, chat_history)
    if "Tool 2" in thought:
        marked_image = toolkit_function.distance_ruler(image, 10)
        cv2.imwrite(f'log/{counter}distance_ruler_image.jpg', marked_image)
        user_input = "This is the image with Distance Ruler. If you have any thought of the process, please let me know to help with you, What to do next?"
        response, chat_history = analyze_image(user_input, marked_image, chat_history)
    if "Tool 3" in thought:
        bounding_box_parameter = thought[1]
        bounding_box_image = toolkit_function.bounding_box(image, thought[1])
        cv2.imwrite(f'log/{counter}bounding_box.jpg', bounding_box_image)
        user_input = "This is the image with Bounding Box. If you have any thought of the process, please let me know to help with you, What to do next?"
        response, chat_history = analyze_image(user_input, bounding_box_image, chat_history)
    if "Tool 4" in thought:
        bounding_box_image = toolkit_function.distance_ruler(bounding_box_image, 10)
        user_input = ROI_examiner(bounding_box_parameter, bounding_box_image)
        response, chat_history = analyze_image(user_input, bounding_box_image, chat_history)
    print("Round", counter, "response:", response)
    thought = thought_extractor(response)
    print("Extracting")
    thought = extract_substrings(thought)
    print("Round", counter, "thought:", thought)

