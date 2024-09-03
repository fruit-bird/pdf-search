import argparse
import requests

# replacing monopoly with another cat
# 51 docs befores


def update_pdf(pdf_path):
    url = "http://localhost:8000/pdf/aa7d836b-e4d2-4577-9c4f-86ee11b60c79"

    with open(pdf_path, "rb") as file:
        files = {"file": (pdf_path, file, "application/pdf")}
        response = requests.put(url, files=files)
        print(response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a PDF file.")
    parser.add_argument(
        "pdf_path",
        type=str,
        help="The path to the PDF file you want to replace",
    )

    args = parser.parse_args()
    update_pdf(args.pdf_path)
