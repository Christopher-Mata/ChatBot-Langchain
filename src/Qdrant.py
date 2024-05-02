"""
    _summary_
        This file is used to create the vector store for the LangchainAgent. 
    
        It uses the qdrant_client library to create the vector store.
        A vector store is a database that stores vectors. It is used to store the vectors of the documents that the AI will use to memorize.
        Vectors are created using Embeddings. In this file, you are using OpenAIEmbeddings which require the OpenAI API key to work.
    
        The vector store of choise is Qdrant, which stores vectors in primary and secondary memory. You can implement another 
        if you choose like PineCone. 
    
        PLEASE PUT YOUR OPEN AI API KEY IN THE .env FILE in the LangchainAgent directory.Like this:
        OPENAI_API_KEY=''
    
        @Author: Christopher Mata
"""

# These are the imports for the qdrant.py file
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_community.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Qdrant

# Loads the .env file for the environment variables
load_dotenv()

def vectorStore():
    """
    This function is used to create the vector store for the LangchainAgent. It uses the qdrant_client library to create the vector store.
    
    Returns:
        QdrantClient: It returns a QdrantClient object that is used to store vectors and by the LLM to query.
    """
    
    # Sets up the API for embeddings, loads the document containing UW Parkside webscraped data, and splits the document into chunks
    # The file LITTERALLY has all the text in all domains regarding UW Parkside. CURRENTLY: it is recomended to use chunks of 1000 characters.
    os.environ["OPENAI_API_KEY"]
    loader = TextLoader("UWParksideData.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # initiates the embeddings to vectorize the text chunks.
    embeddings = OpenAIEmbeddings()

    # Creates the vector store using the qdrant_client library
    # The path indicates that the majority of the vector store will be stored in memory, and the rest will be stored in secondary memory.
    # The collection name is the name of the collection that the vectors will be stored in.
    qdrant = Qdrant.from_documents(
        docs,
        embeddings,
        location=":memory:",
        collection_name="UWParkside_vectorDB",
        force_recreate=True
    )

    # Returns the vector store
    return qdrant