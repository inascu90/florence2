# -*- coding: utf-8 -*-
"""Florence-2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E1XWTEqYdtHj8DbG2rR10CwlOtrR-rMN
"""

import time
import requests

from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

from datetime import datetime

from transformers import AutoProcessor,AutoModelForCausalLM
from PIL import Image
import requests
import copy
import cv2
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.patches as patches
model_id = 'microsoft/Florence-2-large'
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).eval() #method sets the model to evaluation mor processor
processor = AutoProcessor. from_pretrained(model_id, trust_remote_code=True) #The AutoProcessor class is used to process input
#By setting trust_remote_code=True, you are saying it's okay for these custom scripts to run on your computer.

def run_example(task_prompt, text_input=None) :
  if text_input is None:
    prompt = task_prompt
  else:
    prompt = task_prompt + text_input
  inputs = processor(text=prompt,images=image, return_tensors="pt") # It converts both text and images into a format (PyTor #The model generates text based on the processed
  generated_ids = model.generate( input_ids=inputs["input_ids"], pixel_values=inputs["pixel_values"],
  #input ids and pixel_values are the processed text and image inputs.
  max_new_tokens=1024,
  #maximum number of tokens to generate
  early_stopping=False,
  # the model will not stop early based on certain criteria
  do_sample=False,
  num_beams=3,)
  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # float `width`
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
  generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

  parsed_answer = processor.post_process_generation(
    generated_text,
    task=task_prompt,
    image_size=(width,height)#(image.width, image.height)#(1920,1080)
      )
  return parsed_answer
cam_url="park.mp4"
cap = cv2.VideoCapture(cam_url)
i=0
start_time=time.time()
while i<3:
  end_time=time.time()
  if (end_time-start_time)>10:
    start_time=time.time()
    current_time = datetime.now()
    ret, frame = cap.read()
    #task_prompt1 = '<OD>'
    task_prompt2 = '<MORE_DETAILED_CAPTION>'
    
    image=frame
    #results1 = run_example(task_prompt1)#run_example(task_prompt,text_input="A green car parked in front of a yellow building.")
    results2 = run_example(task_prompt2)
   
    #print("The reult of OD is: ",results1)
    caption=results2['<MORE_DETAILED_CAPTION>']
    print("The reult of MORE_DETAILED_CAPTION is: ",caption)
    #save screenshot into file
    screenshot = frame[:]
    screenshot_filename = f'images/florence/{cam_url}-{i}-{current_time.strftime("%Y-%m-%d_%I-%M-%p")}.png'
    txt_flie_name=f'description/{cam_url}-{i}-{current_time.strftime("%Y-%m-%d_%I-%M-%p")}.txt'
    cv2.imwrite(screenshot_filename, screenshot)
    # Write the caption to the file
    with open(txt_flie_name, 'w') as file:
        file.write(caption)
    i+=1
    
