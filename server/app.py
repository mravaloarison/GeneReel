from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gemini import test_call, generate_json_transcript, get_keywords_for_each_sentence
from elevenlabs_tts import text_to_speech_file
from cloudflare import Cloudflare
from PIL import Image
import random, os


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


@app.route("/serve/<filename>")
def serve(filename):
    return send_from_directory("static", filename)


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
        "response": [array, str, array]
    }
    """
    if request.method == "GET":
        return jsonify({"error": "Method not allowed!"})
    
    try:
        files = os.listdir("static")

        for file in files:
            if file.endswith(".png"):
                os.remove(f"static/{file}")
    except Exception:
        ...
    
    data = request.get_json()
    try:
        res = generate_json_transcript(data["prompt"])
        keywords_and_transcript = get_keywords_for_each_sentence(res)

        return jsonify({"response": keywords_and_transcript})
    
    except Exception:
        return jsonify({"error": "Something went wrong while generating transcript!"})
    

@app.route("/generate_image")
def generate_image():
    """
    Generate an image from a given prompt.

    Expected query parameter:
    q: str

    Returns:
    {
        "id": int
    }
    """
    q = request.args.get("q")

    client = Cloudflare(api_token=os.getenv("CLOUDFLARE_API_TOKEN"))
    data = client.workers.ai.with_raw_response.run(
        "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        account_id=os.getenv("CLOUDFLARE_ACCOUNT_ID"),
        prompt= q,
    )

    try:
        img = Image.open(data)

        randomId = random.randint(0, 400)
        img.save(f"static/{str(randomId)}.png")

        return jsonify({"id": randomId})
    
    except Exception:
        return jsonify({"error": "Something went wrong while generating image!"})