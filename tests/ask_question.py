import json
import requests


url = "http://localhost:8000/ask"
question = "what do know about neutering cats"

response = requests.post(url, json={"question": question})
print(json.dumps(response.json()))
