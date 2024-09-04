import yaml
from chromadb import Settings


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

    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class ChromaConfig:
    def __init__(self, host, port):
        self.host: str = host
        self.port: int = port


class AppConfig:
    def __init__(self, ai, api, chroma):
        self.ai = AIConfig(**ai)
        self.api = APIConfig(**api)
        self.chroma = ChromaConfig(**chroma)

    @staticmethod
    def load():
        with open("config.dev.yaml", "r") as f:
            config = yaml.safe_load(f)
        return AppConfig(**config)


config = AppConfig.load()
chroma_config = Settings(
    chroma_server_host=config.chroma.host,
    chroma_server_http_port=config.chroma.port,
)
