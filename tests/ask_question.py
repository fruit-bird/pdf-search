import json
import requests

url = "http://localhost:8000/pdf/ask/"
question = "What should a responsible cat owner ensure for their cat?"

response = requests.post(url, json={"question": question})
print(json.dumps(response.json()))
