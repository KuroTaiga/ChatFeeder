import openai

import requests
#from transformers import LlamaTokenizer, LlamaForCausalLM
from PIL import Image
import torch
import io
import pandas as pd
import os
import base64
import replicate
from llamaapi import LlamaAPI

# Set your API keys
openai.api_key = ""
llama_api_key = ""
openroute_api_key = "" 
REPLICATE_API_TOKEN = ""
# Initialize the SDK
#llama = LlamaAPI(llama_api_key)
llamaAPI_client = openai.OpenAI(
    api_key = llama_api_key,
    base_url = "https://api.llama-api.com"
)
openroute_client = openai.OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = openroute_api_key
)



# Define the paths
folder_path = "./blender_pics_final"
test_run_folder_path = "./test_run"
#prompt = "This is an iamge that contains 3 seperate frames from a blender render of a workout activity. Discribe in detail the body movement of the activity."
Xiang_prompt = "Please provide a single-paragraph summary of the sequence of poses, integrating the key actions and body positions into a fluid, continuous description. Avoid breaking the description into separate positions, and focus on capturing the seamless flow of movement and the overall effect on the body. For reference, here are a few examples of the style and structure expected: 'Stand behind a bench, with the chest leaning over the edge of the bench. With one arm resting on the bench, hold the kettlebell, bending the arm at the elbow. Lower the arm using the bench as a guide, keeping the forearm straight.' 'The user stands, both hands holding a kettlebell, moving it toward the face, then returning it to the wrist.' 'Upper arms stable, curl the weights forward until the barbell reaches shoulder level. Lower the weight back to the starting position.' 'The person stands upright with legs together, arms extended above the head, palms facing inward. The head follows the line of the arms, with eyes gazing upward.' Ensure the summary captures the entire sequence as one continuous motion rather than separate steps."
system_prompt = "You are to describe the activity based one the image provided. The image is in base64 encoded format."
llama_prompt = "Can you take image as input?"
# 1. Convert image to bytes (for API or model input)
def load_image_as_bytes(image_path):
    with open(image_path, 'rb') as img_file:
        return img_file.read()
def encode_image(image_path):
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# 2. Send image and prompt to ChatGPT-4
def send_to_chatgpt(image, prompt):
    response = openai.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text":prompt},
                {"type":"image_url",
                 "image_url":{
                     "url":f"data:image/png;base64,{image}"
                 }}]}
        ],
    )

    return response.choices[0].message.content

# 3. Send image and prompt to LLaMA 3.1
def send_to_llama(image, prompt):
    image_url = f"data:image/png;base64,{image}"
    #print(image_url)
    response = openroute_client.chat.completions.create(
        model="meta-llama/llama-3.1-405b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/png;base64,{image}"
                    }
                }
                ]
            }

        ],
    )
    return response.choices[0].message.content

def send_to_llama_replic(image_path,prompt):
    image = open(image_path, "rb")
    output = replicate.run(
        "meta/meta-llama-3.1-405b-instruct",
        input={
            "image": image,
            "system_prompt":system_prompt,
            "prompt": Xiang_prompt
        }
    )
    return output



# 4. Save responses to an Excel sheet
def save_to_excel(chatgpt_response, llama_response, excel_file="responses.xlsx"):
    # Create a DataFrame with responses
    df1 = pd.DataFrame.from_dict(chatgpt_response,orient = 'index', columns=['Activity','Chat_Response'])
    df2 = pd.DataFrame.from_dict(llama_response,orient = 'index',columns = ['Activity','Llama_Response'])
    df = pd.merge(df1,df2,on= 'Activity',how='left')
    
    
    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)
    print(f"Responses saved to {excel_file}")

# 5. Run both models and save responses
def process_images_from_folder(folder_path, prompt, excel_file="responses.xlsx"):
    # Initialize a list to hold all data for the Excel sheet
    openai_response_dict = dict()
    llama_response_dict = dict()
    
    #Loop through all PNG files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".png"):
            image_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")

            # Load image
            image_base64 = encode_image(image_path)
            
            # Send prompt to ChatGPT-4
            chatgpt_response = send_to_chatgpt(image_base64,prompt)
            print(f"ChatGPT-4 Response for {file_name}: {chatgpt_response}")
            # Append results to data list
            # data.append({
            #     "Image": file_name,
            #     "Model": "ChatGPT-4",
            #     "Response": chatgpt_response
            # })
            openai_response_dict[file_name[:-4]] = [file_name[:-4],chatgpt_response]
    
    # for file_name in os.listdir(folder_path):
    #     if file_name.endswith(".png"):
    #         image_path = os.path.join(folder_path, file_name)
    #         print(f"Processing {file_name}...")

    #         # Load image
    #         image_base64 = encode_image(image_path)        
            # # Send prompt to LLaMA 3.1
            # llama_response = send_to_llama(image_base64,prompt)
            # print(f"LLaMA 3.1 Response for {file_name}: {llama_response}")

            # llama_response_dict[file_name[:-4]] = [file_name[:-4],llama_response]

    # Save all data to Excel
    save_to_excel(openai_response_dict, llama_response_dict,excel_file = excel_file)

# Example usage
process_images_from_folder(folder_path, prompt = Xiang_prompt)
# process_images_from_folder(folder_path=test_run_folder_path, prompt=Xiang_prompt, excel_file="testrun.xlsx")
