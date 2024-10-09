import requests, os
from dotenv import load_dotenv

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

load_dotenv()

def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"

    headers = {
        "Accept": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    for voice in data['voices']:
        print(f"{voice['name']}: {voice['voice_id']}")


def text_to_speech_file(text: str) -> str:
    client = ElevenLabs(
        api_key = os.getenv("ELEVENLABS_API_KEY"),
    )

    response = client.text_to_speech.convert(
        voice_id = os.getenv("ELEVENLABS_VOICE_ID"), 
        output_format = "mp3_22050_32",
        text = text,
        model_id = "eleven_turbo_v2_5", 
        voice_settings = VoiceSettings(
            stability = 0.5,
            similarity_boost = 0.8,
            style = 1.0,
            use_speaker_boost = True,
        ),
    )

    save_file_path = "static/voiceover.mp3"

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    return save_file_path

# text_to_speech_file("Hello, my name is John. I am a software engineer.")