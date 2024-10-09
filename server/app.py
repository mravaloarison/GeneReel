from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import test_call, generate_json_transcript, get_keywords_for_each_sentence
from elevenlabs_tts import text_to_speech_file


app = Flask(__name__)


CORS(app)


@app.route("/")
def index():
    return jsonify({"message": "Server says Hi!"})


@app.route("/ping")
def ping():
    return jsonify({"message": "Pong!"})


@app.route("/hi_gemini")
def hi_gemini():
    res = test_call("Say Hi!")

    return jsonify({"response": res})


@app.route("/create_voiceover", methods = ["POST", "GET"])
def create_voiceover():
    """
    Create a voiceover from a given transcript.

    Expected JSON format:
    {
        "transcript": str
    }

    Returns:
    {
        "message": str
    }
    """
    if request.method == "GET":
        return jsonify({"error": "Please send a POST request!"})
    
    data = request.get_json()
    try:
        text_to_speech_file(data["transcript"])
        return jsonify({"message": "Voiceover created successfully!"})
    
    except Exception:
        return jsonify({"error": "Something went wrong while creating voiceover!"})
    
    
@app.route("/generate_transcript", methods = ["POST", "GET"])
def generate_transcript():
    """
    Generate a transcript from a given prompt.

    Expected JSON format:
    {
        "prompt": str
    }

    Returns:
    {
        "response": [keywords, transcript]
    }
    """
    if request.method == "GET":
        return jsonify({"error": "Method not allowed!"})
    
    data = request.get_json()
    try:
        res = generate_json_transcript(data["prompt"])
        keywords_and_transcript = get_keywords_for_each_sentence(res)

        return jsonify({"response": keywords_and_transcript})
    
    except Exception:
        return jsonify({"error": "Something went wrong while generating transcript!"})
