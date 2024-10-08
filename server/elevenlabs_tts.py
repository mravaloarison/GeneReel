import requests, os
from dotenv import load_dotenv
from config import ELEVENLABS_API_KEY

load_dotenv()

url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
  "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
  "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

data = response.json()
for voice in data['voices']:
    print(f"{voice['name']}; {voice['voice_id']}")
