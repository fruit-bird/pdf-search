<!-- some_name.pdf -> STORAGE/uuid.pdf
              -> metadata: {
                        name: some_name.pdf,
                        source: STORAGE/uuid.pdf,
                    }

---

# when processing a pdf file to embeddings in the db,
# make it a background task -->

# PDF Q&A API

A REST API that allows users to upload PDF files, and generate text embeddings in a vector database, and provides a search mechanism to answer questions based on the content of the PDFs

## Startup Instructions
1. Clone the repository

    ```sh
    git clone https://github.com/fruit-bird/pdf-search.git
    cd pdf-search
    ```

2. Set up your Google API key

    - Open `config.dev.yaml`
    - Add your key

        ```yaml
        ai:
          google_api_key: "my_google_api_key"
        ```

3. Start the application:
    
    ```sh
    docker-compose up
    ```

The API should be accessible at the port specified in the `config.dev.yaml` file under `api.port`, by default it is `8080`

## Design Documentation
### Tech Stack
- **Framework**: FastAPI (Python)
- **Vector Database**: ChromaDB


### Project Structure
- `config.dev.yaml`: Contains the configuration for the application
- `pdf_search/`: Contains the main application code
    - `routes/`: Contains the API routes
    - `services/`: Contains the services that are called in the routes
    - `schemas/`: Contains the Pydantic models
    - `config.py`: Reads the configuration file `config.dev.yaml`
    - `main.py`: The entry point of the application


### Design Choices
Instead of storing the metadata in a traditional database, we store the embeddings in a vector database (ChromaDB) and attach the metadata to the embeddings. This allows us to know the source of the embeddings and retrieve or filter by the source when needed


The typical flow of the application is as follows:

#### PDF Upload
- User uploads a PDF
- System generates a UUID
- PDF is renamed to UUID.pdf and saved in the `api.pdf_storage_path` directory
- Text is extracted from the PDF
- Embeddings are generated from the extracted text
- Metadata pointing to the originating PDF is attached to the embeddings
- Embeddings and metadata are stored in ChromaDB

#### Question Answering ([example](#example))
- User submits a question
- System generates an embedding for the question
- ChromaDB is queried to find relevant document chunks
- LLM uses the relevant chunks to generate an answer while staying within the context of the document


### API Documentation
The API documentation is automatically generated and can be accessed at `/docs` when the server is running


## Example
`POST /v1/ask` (assuming the user uploaded a document with the Monopoly rules)
```json
{"question": "how much money do you start with in a game of monopoly"}
```

Response:
```json
{
  "question": "how much money do you start with in a game of monopoly",
  "answer": "According to the context, each player starts with $1,500 divided as follows: 2 each of $500s, 10 each of $100s and $50s, 6 each of $40s, 5 each of $10s, $5s and $1s.",
  "sources": [
    "a63948aa-1060-4244-871e-68072319a0ac",
    "a63948aa-1060-4244-871e-68072319a0ac",
    "a63948aa-1060-4244-871e-68072319a0ac",
    "a63948aa-1060-4244-871e-68072319a0ac"
  ],
  "names": [
    "monopoly_rules.pdf",
    "monopoly_rules.pdf",
    "monopoly_rules.pdf",
    "monopoly_rules.pdf"
  ]
}
```
