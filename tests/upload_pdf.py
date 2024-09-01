import json
import requests


pdf_path = "eg01_caring_for_your_cat.pdf"
url = "http://localhost:8000/pdf/upload"

with open(pdf_path, "rb") as file:
    files = {"file": (pdf_path, file, "application/pdf")}
    response = requests.post(url, files=files)
    print(json.dumps(response.json()))
