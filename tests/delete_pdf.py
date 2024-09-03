import json
import requests

url = "http://localhost:8000/pdf/749eb72e-1455-4a28-9de6-f59056edf671"

response = requests.delete(url)
print(json.dumps(response.json(), indent=4))
