import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()

from config import generate_json_response_prompt, get_keywords_for_each_sentence_prompt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt_to_json_model = genai.GenerativeModel("gemini-1.5-flash", 
    generation_config = {"response_mime_type": "application/json"})
regular_model = genai.GenerativeModel("gemini-1.5-flash")

def generate_json_script(userPrompt):
    prompt = generate_json_response_prompt + userPrompt

    response = prompt_to_json_model.generate_content(prompt)
    response = json.loads(response.text)

    return response

def get_keywords_for_each_sentence(script):
    transcript = ""

    for sentence in script:
        transcript += sentence[0] + " "

    prompt = get_keywords_for_each_sentence_prompt + transcript

    response = prompt_to_json_model.generate_content(prompt)
    res = json.loads(response.text)

    return [res, transcript]

