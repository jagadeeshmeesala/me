import json
import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
import hashlib
from collections import defaultdict

class AnalyticsService:
    def __init__(self):
        self.data_file = "data/analytics.json"
        self.visitors_file = "data/visitors.json"
        self._ensure_data_directory()
        self._load_data()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        os.makedirs("data", exist_ok=True)
    
    def _load_data(self):
        """Load analytics data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.analytics_data = json.load(f)
            else:
                self.analytics_data = {
                    "total_visitors": 0,
                    "unique_visitors": 0,
                    "page_views": 0,
                    "daily_stats": {},
                    "visitor_sessions": []
                }
                self._save_data()
            
            if os.path.exists(self.visitors_file):
                with open(self.visitors_file, 'r') as f:
                    self.visitors_data = json.load(f)
            else:
                self.visitors_data = {
                    "unique_visitors": [],
                    "visitor_ips": {}
                }
                self._save_visitors()
                
        except Exception as e:
            print(f"Error loading analytics data: {e}")
            self.analytics_data = {
                "total_visitors": 0,
                "unique_visitors": 0,
                "page_views": 0,
                "daily_stats": {},
                "visitor_sessions": []
            }
            self.visitors_data = {
                "unique_visitors": [],
                "visitor_ips": {}
            }
    
    def _save_data(self):
        """Save analytics data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.analytics_data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics data: {e}")
    
    def _save_visitors(self):
        """Save visitors data to file"""
        try:
            with open(self.visitors_file, 'w') as f:
                json.dump(self.visitors_data, f, indent=2)
        except Exception as e:
            print(f"Error saving visitors data: {e}")
    
    def track_visit(self, ip_address: str, user_agent: str = "", page: str = "/") -> Dict[str, Any]:
        """Track a new visit"""
        today = date.today().isoformat()
        visitor_id = self._generate_visitor_id(ip_address, user_agent)
        
        # Check if this is a new unique visitor
        is_new_visitor = visitor_id not in self.visitors_data["unique_visitors"]
        
        if is_new_visitor:
            self.visitors_data["unique_visitors"].append(visitor_id)
            self.analytics_data["unique_visitors"] = len(self.visitors_data["unique_visitors"])
        
        # Increment total visitors
        self.analytics_data["total_visitors"] += 1
        self.analytics_data["page_views"] += 1
        
        # Update daily stats
        if today not in self.analytics_data["daily_stats"]:
            self.analytics_data["daily_stats"][today] = {
                "visitors": 0,
                "page_views": 0,
                "unique_visitors": set()
            }
        
        self.analytics_data["daily_stats"][today]["visitors"] += 1
        self.analytics_data["daily_stats"][today]["page_views"] += 1
        self.analytics_data["daily_stats"][today]["unique_visitors"].add(visitor_id)
        
        # Record session
        session = {
            "visitor_id": visitor_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "page": page,
            "timestamp": datetime.now().isoformat(),
            "is_new_visitor": is_new_visitor
        }
        
        self.analytics_data["visitor_sessions"].append(session)
        
        # Keep only last 1000 sessions to prevent file from growing too large
        if len(self.analytics_data["visitor_sessions"]) > 1000:
            self.analytics_data["visitor_sessions"] = self.analytics_data["visitor_sessions"][-1000:]
        
        # Save data
        self._save_data()
        self._save_visitors()
        
        return {
            "total_visitors": self.analytics_data["total_visitors"],
            "unique_visitors": self.analytics_data["unique_visitors"],
            "page_views": self.analytics_data["page_views"],
            "is_new_visitor": is_new_visitor,
            "today_visitors": self.analytics_data["daily_stats"][today]["visitors"],
            "today_unique_visitors": len(self.analytics_data["daily_stats"][today]["unique_visitors"])
        }
    
    def _generate_visitor_id(self, ip_address: str, user_agent: str) -> str:
        """Generate a unique visitor ID based on IP and user agent"""
        combined = f"{ip_address}:{user_agent}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current analytics statistics"""
        today = date.today().isoformat()
        
        # Convert sets to lists for JSON serialization
        daily_stats = {}
        for date_str, stats in self.analytics_data["daily_stats"].items():
            daily_stats[date_str] = {
                "visitors": stats["visitors"],
                "page_views": stats["page_views"],
                "unique_visitors": len(stats["unique_visitors"])
            }
        
        return {
            "total_visitors": self.analytics_data["total_visitors"],
            "unique_visitors": self.analytics_data["unique_visitors"],
            "page_views": self.analytics_data["page_views"],
            "today_visitors": daily_stats.get(today, {}).get("visitors", 0),
            "today_unique_visitors": daily_stats.get(today, {}).get("unique_visitors", 0),
            "daily_stats": daily_stats,
            "recent_sessions": self.analytics_data["visitor_sessions"][-10:]  # Last 10 sessions
        }
    
    def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get daily statistics for the last N days"""
        today = date.today()
        daily_stats = []
        
        for i in range(days):
            check_date = today - timedelta(days=i)
            date_str = check_date.isoformat()
            
            if date_str in self.analytics_data["daily_stats"]:
                stats = self.analytics_data["daily_stats"][date_str]
                daily_stats.append({
                    "date": date_str,
                    "visitors": stats["visitors"],
                    "page_views": stats["page_views"],
                    "unique_visitors": len(stats["unique_visitors"])
                })
            else:
                daily_stats.append({
                    "date": date_str,
                    "visitors": 0,
                    "page_views": 0,
                    "unique_visitors": 0
                })
        
        return list(reversed(daily_stats))  # Return in chronological order

