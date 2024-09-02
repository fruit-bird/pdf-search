import json
import requests
import argparse


def upload_pdf(pdf_path):
    url = "http://localhost:8000/pdf"

    with open(pdf_path, "rb") as file:
        files = {"file": (pdf_path, file, "application/pdf")}
        response = requests.post(url, files=files)
        print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a PDF file to a server.")
    parser.add_argument(
        "pdf_path",
        type=str,
        help="The path to the PDF file you want to upload",
    )

    args = parser.parse_args()
    upload_pdf(args.pdf_path)
