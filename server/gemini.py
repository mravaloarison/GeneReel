import google.generativeai as genai
import os, json
from config import generate_json_response_prompt, get_keywords_for_each_sentence_prompt

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt_to_json_model = genai.GenerativeModel("gemini-1.5-flash", 
    generation_config = {"response_mime_type": "application/json"})
regular_model = genai.GenerativeModel("gemini-1.5-flash")

def generate_json_transcript(userPrompt):
    """
    Generate a transcript from a given prompt.
    """
    prompt = generate_json_response_prompt + userPrompt

    response = prompt_to_json_model.generate_content(prompt)
    response = json.loads(response.text)

    return response

def get_keywords_for_each_sentence(script):
    """
    Generate a keyword for each sentence in the transcript provided later.
    """
    transcript = ""
    array_of_transcript = []

    for sentence in script:
        transcript += sentence[0] + " "
        array_of_transcript.append(sentence[0])

    prompt = get_keywords_for_each_sentence_prompt + transcript

    response = prompt_to_json_model.generate_content(prompt)
    array_of_keywords = json.loads(response.text)

    return [array_of_keywords, transcript, array_of_transcript]

def test_call(prompt):
    response = regular_model.generate_content(prompt)
    return response.text
