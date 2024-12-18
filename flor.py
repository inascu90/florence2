# -*- coding: utf-8 -*-
"""Florence-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E1XWTEqYdtHj8DbG2rR10CwlOtrR-rMN
"""

import os
import time
import requests
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
from datetime import datetime
import copy
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define model and processor
model_id = 'microsoft/Florence-2-large'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval()
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

def run_example(task_prompt, image, text_input=None):
    prompt = task_prompt if text_input is None else task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        early_stopping=False,
        do_sample=False,
        num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    
    width = image.shape[1]
    height = image.shape[0]
    
    parsed_answer = processor.post_process_generation(
        generated_text,
        task=task_prompt,
        image_size=(width, height)
    )
    return parsed_answer

# Define video source
cam_url ="lift1.jpg" #"lifting3.mp4"
cam_url_path = f"{cam_url}"
cap = cv2.VideoCapture(cam_url_path)
# Ensure directories exist
os.makedirs('images/florence', exist_ok=True)
os.makedirs('description', exist_ok=True)
#####
i = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if ret:
        if i % 100 != 0:
            i += 1
            continue
        else:
            start_time = time.time()
            current_time = datetime.now()
            
            task_prompt2 = '<MORE_DETAILED_CAPTION>'
            
            image = frame
            results2 = run_example(task_prompt2, image)
            
            caption = results2['<MORE_DETAILED_CAPTION>']
            print("The result of MORE_DETAILED_CAPTION is: ", caption)
            
            # Save screenshot to file
            screenshot = frame[:]
            screenshot_filename = f'images/florence/{cam_url}-{i}-{current_time.strftime("%Y-%m-%d_%I-%M-%p")}.png'
            txt_file_name = f'description/{cam_url}-{i}-{current_time.strftime("%Y-%m-%d_%I-%M-%p")}.txt'
            
            cv2.imwrite(screenshot_filename, screenshot)
            with open(txt_file_name, 'w') as file:
                file.write(f"{current_time.strftime('%Y-%m-%d_%I-%M-%p')} \n {caption} \n The image url is: {screenshot_filename}")
            
            i += 1
    else:
        print("video ended")
        break
