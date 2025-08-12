from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.search_service import SearchService
import logging

router = APIRouter()
search_service = SearchService()

class SearchRequest(BaseModel):
    query: str

class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    score: float
    url: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int
    query: str

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Perform AI-powered search on the knowledge base
    """
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Perform search using the search service
        results = await search_service.search(request.query.strip())
        
        return SearchResponse(
            results=results,
            total_results=len(results),
            query=request.query
        )
        
    except Exception as e:
        logging.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during search")

@router.get("/search/suggestions")
async def get_search_suggestions(q: str):
    """
    Get search suggestions based on partial query
    """
    try:
        if not q.strip():
            return {"suggestions": []}
        
        suggestions = await search_service.get_suggestions(q.strip())
        return {"suggestions": suggestions}
        
    except Exception as e:
        logging.error(f"Search suggestions error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/popular")
async def get_popular_searches():
    """
    Get popular search terms
    """
    try:
        popular_searches = await search_service.get_popular_searches()
        return {"popular_searches": popular_searches}
        
    except Exception as e:
        logging.error(f"Popular searches error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
