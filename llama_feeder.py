import openai
import requests
#from transformers import LlamaTokenizer, LlamaForCausalLM
from PIL import Image
import torch
import io
import pandas as pd
import os
import base64
# Set your API keys
openai.api_key = 

# Define the paths
folder_path = "./blender_pics_final"
test_run_folder_path = "./test_run"
prompt = "This is an iamge that contains 3 seperate frames from a blender render of a workout activity. Discribe in detail the body movement of the activity."

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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are to discribe the activity based one the image provided."},
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
def send_to_llama(image_bytes, prompt):
    tokenizer = LlamaTokenizer.from_pretrained('huggingface/LLaMA-3B')
    model = LlamaForCausalLM.from_pretrained('huggingface/LLaMA-3B')
    
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate text output
    with torch.no_grad():
        outputs = model.generate(input_ids=inputs["input_ids"], max_length=50)
    
    # Decode the response from the model
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return output_text

# 4. Save responses to an Excel sheet
def save_to_excel(chatgpt_response, llama_response, excel_file="responses.xlsx"):
    # Create a DataFrame with responses
    df = pd.DataFrame({
        "Model": ["ChatGPT-4", "LLaMA 3.1"],
        "Response": [chatgpt_response, llama_response]
    })
    
    # Save the DataFrame to an Excel file
    df.to_excel(excel_file, index=False)
    print(f"Responses saved to {excel_file}")

# 5. Run both models and save responses
def process_images_from_folder(folder_path, prompt, excel_file="responses.xlsx"):
    # Initialize a list to hold all data for the Excel sheet
    data = []
    
    # Loop through all PNG files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".png"):
            image_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")

            # Load image as bytes
            image_bytes = load_image_as_bytes(image_path)
            image_base64 = encode_image(image_path)
            
            # Send prompt to ChatGPT-4
            chatgpt_response = send_to_chatgpt(image_base64,prompt)
            print(f"ChatGPT-4 Response for {file_name}: {chatgpt_response}")
            
            # # Send prompt to LLaMA 3.1
            # llama_response = send_to_llama(prompt)
            # print(f"LLaMA 3.1 Response for {file_name}: {llama_response}")
            
            # Append results to data list
            data.append({
                "Image": file_name,
                "Model": "ChatGPT-4",
                "Response": chatgpt_response
            })
            # data.append({
            #     "Image": file_name,
            #     "Model": "LLaMA 3.1",
            #     "Response": llama_response
            # })
    
    # Save all data to Excel
    save_to_excel(data, excel_file)

# Example usage
#process_images_from_folder(folder_path, prompt)
process_images_from_folder(folder_path=test_run_folder_path, prompt=prompt, excel_file="testrun.xlsx")
