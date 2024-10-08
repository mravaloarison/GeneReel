import requests
import os
from config import ELEVENLABS_API_KEY

url = "https://api.elevenlabs.io/v1/voices"

headers = {
  "Accept": "application/json",
  "xi-api-key": ELEVENLABS_API_KEY,
  "Content-Type": "application/json"
}

# A GET request is sent to the API endpoint. The URL and the headers are passed into the request.
response = requests.get(url, headers=headers)

# The JSON response from the API is parsed using the built-in .json() method from the 'requests' library. 
# This transforms the JSON data into a Python dictionary for further processing.
data = response.json()

# A loop is created to iterate over each 'voice' in the 'voices' list from the parsed data. 
# The 'voices' list consists of dictionaries, each representing a unique voice provided by the API.
for voice in data['voices']:
  # For each 'voice', the 'name' and 'voice_id' are printed out. 
  # These keys in the voice dictionary contain values that provide information about the specific voice.
  print(f"{voice['name']}; {voice['voice_id']}")
