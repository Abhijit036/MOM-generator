import google.generativeai as genai
import cv2
import os
from PIL import Image

def extract_text_from_image(image_path):
    image=cv2.imread(r'C:\Users\abhij\Documents\GLclassroom\InClass\GenAI\MoM Generator\New2.jpg')
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # Convert BGR to RGB
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # Convert BGR to Grey
    _, image_bw = cv2.threshold(image_grey, 150, 255, cv2.THRESH_BINARY) # Convert grey to Binary using thresholding

    final_image=Image.fromarray(image_bw) # Convert array to Image

# Configure Genai model
    key=os.getenv('GOOGLE_  API_KEY')
    genai.configure(api_key=key)
    model=genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets write a prompt for OCR
    prompt='''You act as an OCR application on the given image and extract the text from it.
            Give only the text as output without any other explanation or description.'''

#Lets run and extract and return the text    
    response=model.generate_content([prompt,final_image])
    output_text=response.text
    return output_text