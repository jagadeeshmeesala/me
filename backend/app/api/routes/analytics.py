from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.analytics_service import AnalyticsService
import logging

router = APIRouter()
analytics_service = AnalyticsService()

class VisitRequest(BaseModel):
    page: str = "/"
    user_agent: str = ""

class AnalyticsResponse(BaseModel):
    total_visitors: int
    unique_visitors: int
    page_views: int
    today_visitors: int
    today_unique_visitors: int
    daily_stats: Dict[str, Any]

@router.post("/track-visit")
async def track_visit(request: Request, visit_data: VisitRequest):
    """
    Track a new visit to the website
    """
    try:
        # Get client IP address
        client_ip = request.client.host
        
        # Get user agent from request headers
        user_agent = request.headers.get("user-agent", visit_data.user_agent)
        
        # Track the visit
        result = analytics_service.track_visit(
            ip_address=client_ip,
            user_agent=user_agent,
            page=visit_data.page
        )
        
        return {
            "success": True,
            "message": "Visit tracked successfully",
            "data": result
        }
        
    except Exception as e:
        logging.error(f"Error tracking visit: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to track visit")

@router.get("/stats", response_model=AnalyticsResponse)
async def get_analytics_stats():
    """
    Get current analytics statistics
    """
    try:
        stats = analytics_service.get_stats()
        return AnalyticsResponse(**stats)
        
    except Exception as e:
        logging.error(f"Error getting analytics stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get analytics stats")

@router.get("/daily-stats")
async def get_daily_stats(days: int = 7):
    """
    Get daily statistics for the last N days
    """
    try:
        if days < 1 or days > 30:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 30")
        
        daily_stats = analytics_service.get_daily_stats(days)
        return {
            "success": True,
            "data": daily_stats,
            "days_requested": days
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting daily stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get daily stats")

@router.get("/visitor-count")
async def get_visitor_count():
    """
    Get simple visitor count for display on website
    """
    try:
        stats = analytics_service.get_stats()
        return {
            "total_visitors": stats["total_visitors"],
            "unique_visitors": stats["unique_visitors"],
            "today_visitors": stats["today_visitors"]
        }
        
    except Exception as e:
        logging.error(f"Error getting visitor count: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get visitor count")

@router.post("/reset-stats")
async def reset_analytics():
    """
    Reset all analytics data (admin only)
    """
    try:
        # In a real application, you'd add authentication here
        analytics_service.analytics_data = {
            "total_visitors": 0,
            "unique_visitors": 0,
            "page_views": 0,
            "daily_stats": {},
            "visitor_sessions": []
        }
        analytics_service.visitors_data = {
            "unique_visitors": [],
            "visitor_ips": {}
        }
        
        analytics_service._save_data()
        analytics_service._save_visitors()
        
        return {
            "success": True,
            "message": "Analytics data reset successfully"
        }
        
    except Exception as e:
        logging.error(f"Error resetting analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to reset analytics")

