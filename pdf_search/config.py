import yaml


class DatabaseConfig:
    def __init__(self, host, port, username, password, db_name):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.db_name: str = db_name

    def url(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class AIConfig:
    def __init__(self, model_name, num_tokens, openai_api_key):
        self.model_name: str = model_name
        self.num_tokens: int = num_tokens
        self.openai_api_key: str = openai_api_key


class APIConfig:
    def __init__(self, host, port, pdf_storage_path):
        self.host: str = host
        self.port: int = port
        self.pdf_storage_path: str = pdf_storage_path


class S3Config:
    def __init__(self, port, access_key, secret_key, bucket_name, region):
        self.port: int = port
        self.access_key: str = access_key
        self.secret_key: str = secret_key
        self.bucket_name: str = bucket_name
        self.region: str = region

    def url(self) -> str:
        return f"s3://{self.bucket_name}"


class AppConfig:
    def __init__(self, database, ai, api, s3):
        self.database = DatabaseConfig(**database)
        self.ai = AIConfig(**ai)
        self.api = APIConfig(**api)
        self.s3 = S3Config(**s3)

    def load():
        with open("config.dev.yaml", "r") as f:
            config = yaml.safe_load(f)
        return AppConfig(**config)


config = AppConfig.load()

# class Settings(BaseSettings):
#     DATABASE_URL: str = os.getenv(
#         "DATABASE_URL", "postgresql://user:password@localhost/pdf_search"
#     )
#     OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
#     PDF_STORAGE_PATH: str = os.getenv("PDF_STORAGE_PATH", "./bucket")
#     # PDF_STORAGE_PATH: str = os.getenv("PDF_STORAGE_PATH", "s3://your-bucket-name/pdfs")

#     class Config:
#         env_file = ".env"


# settings = Settings()
