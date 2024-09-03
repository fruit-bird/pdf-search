import yaml


class AIConfig:
    def __init__(self, model_name, embedding_model_name, google_api_key):
        self.model_name: str = model_name
        self.embedding_model_name: str = embedding_model_name
        self.google_api_key: str = google_api_key


class APIConfig:
    def __init__(self, host, port, pdf_storage_path, embeddings_persist_path):
        self.host: str = host
        self.port: int = port
        self.pdf_storage_path: str = pdf_storage_path
        self.embeddings_persist_path: str = embeddings_persist_path


class AppConfig:
    def __init__(self, ai, api):
        self.ai = AIConfig(**ai)
        self.api = APIConfig(**api)

    def load():
        with open("config.dev.yaml", "r") as f:
            config = yaml.safe_load(f)
        return AppConfig(**config)


config = AppConfig.load()
