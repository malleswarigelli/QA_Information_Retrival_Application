from llama_index.core import VectorStoreIndex
from llama_index.core import ServiceContext
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.gemini import GeminiEmbedding

from QAWithPDF.data_ingestion import load_data
from QAWithPDF.model_api import load_model

import sys
from exception import customexception
from logger import logging

def download_gemini_embedding(model,document):
    """
    Downloads and initializes a Gemini Embedding model for vector embeddings.
    Params: 
    model: embedding model
    document: data
    
    Returns:
    - VectorStoreIndex: An index of vector embeddings for efficient similarity queries.
    """
    try:
        logging.info("Embedding started!")
        gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")
        logging.info(f"Gemini Embedding Model loaded: {gemini_embed_model}")
        logging.info("Configure service context")
        service_context = ServiceContext.from_defaults(llm=model,embed_model=gemini_embed_model, chunk_size=800, chunk_overlap=20)
        
        logging.info("Indexing")
        index = VectorStoreIndex.from_documents(document,service_context=service_context)
        logging.info("store the vector embedding index to local database")
        index.storage_context.persist()
        
        logging.info("Querying")
        query_engine = index.as_query_engine()
        return query_engine
    except Exception as e:
        raise customexception(e,sys)


