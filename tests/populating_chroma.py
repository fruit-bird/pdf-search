from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader, DirectoryLoader


loader = DirectoryLoader(
    path="bucket/",
    glob="*.pdf",
    loader_cls=PDFMinerLoader,
)

documents = loader.load()

# basically splits the text into chunks, wow who would have thought lol
text_spplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_spplitter.split_documents(documents)

embedding = OllamaEmbeddings(model="mistral")
vectordb = Chroma.from_documents(
    documents=texts,
    embedding=embedding,
    persist_directory="chroma-db",
)  # auto-persists to disk
