# Import necessary libraries
import os
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load environment variables
load_dotenv()

# Function to load and parse HTML files
def load_html_documents(root_directory: str) -> list:
    """
    This function loads and parses HTML files from a given directory.
    
    Args:
    root_directory (str): The path to the directory containing HTML files.
    
    Returns:
    list: A list of loaded and parsed HTML documents.
    """
    documents = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                loader = UnstructuredHTMLLoader(file_path)
                raw_documents = loader.load()
                documents.extend(raw_documents)
    return documents

# Function to split documents into chunks
def split_documents(documents: list, chunk_size: int, chunk_overlap: int) -> list:
    """
    This function splits documents into chunks of a specified size with a specified overlap.
    
    Args:
    documents (list): A list of documents to be split.
    chunk_size (int): The size of each chunk.
    chunk_overlap (int): The overlap between chunks.
    
    Returns:
    list: A list of split documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_documents = text_splitter.split_documents(documents)
    return split_documents

# Function to update document metadata
def update_document_metadata(documents: list) -> None:
    """
    This function updates the metadata of documents by replacing the source URL.
    
    Args:
    documents (list): A list of documents whose metadata needs to be updated.
    """
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("express-docs", "https:/")
        doc.metadata.update({"source": new_url})

# Function to add documents to Pinecone vector store
def add_documents_to_pinecone(documents: list, embeddings, index_name: str) -> None:
    """
    This function adds documents to the Pinecone vector store.
    
    Args:
    documents (list): A list of documents to be added.
    embeddings: The embeddings model used to convert documents to vectors.
    index_name (str): The name of the index in the Pinecone vector store.
    """
    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
    print("****Loading to vectorstore done ***")

if __name__ == "__main__":
    print("Retrieving ...")

    # Load and parse HTML documents
    directory_path = "express-docs/expressjs.com"
    documents = load_html_documents(directory_path)

    # Split documents into chunks
    chunk_size = 600
    chunk_overlap = 50
    documents = split_documents(documents, chunk_size, chunk_overlap)

    # Update document metadata
    update_document_metadata(documents)

    # Convert documents to embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Add documents to the vector store
    index_name = os.environ["INDEX_NAME"]
    add_documents_to_pinecone(documents, embeddings, index_name)