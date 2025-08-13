from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.rag_service import RAGService
import os

router = APIRouter()
rag_service = RAGService()

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class SearchResult(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    query: str

@router.post("/search", response_model=SearchResult)
async def search(request: SearchRequest):
    """
    Enhanced AI search using RAG (Retrieval-Augmented Generation)
    """
    try:
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            # Fallback to simple search if OpenAI is not configured
            return SearchResult(
                answer="AI search is not configured. Please contact the administrator.",
                sources=[],
                confidence=0.0,
                query=request.query
            )
        
        # Use RAG service for intelligent search
        result = rag_service.search_and_generate(
            query=request.query,
            max_results=request.max_results
        )
        
        return SearchResult(
            answer=result["answer"],
            sources=result["sources"],
            confidence=result["confidence"],
            query=request.query
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/initialize-rag")
async def initialize_rag():
    """
    Initialize the RAG system with sample data
    """
    try:
        rag_service.initialize_sample_data()
        return {"message": "RAG system initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG initialization failed: {str(e)}")

@router.post("/add-document")
async def add_document(content: str, metadata: Dict[str, Any]):
    """
    Add a new document to the RAG system
    """
    try:
        doc_id = rag_service.add_document(content, metadata)
        return {"message": "Document added successfully", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add document: {str(e)}")
