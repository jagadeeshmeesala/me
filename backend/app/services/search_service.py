import asyncio
import json
import os
from typing import List, Dict, Any
from app.core.config import settings
import logging

class SearchService:
    def __init__(self):
        self.search_index = self._load_search_index()
        self.popular_searches = [
            "React development",
            "FastAPI backend",
            "Machine learning",
            "Cloud deployment",
            "Web development",
            "API design",
            "Database optimization",
            "Frontend frameworks"
        ]
    
    def _load_search_index(self) -> List[Dict[str, Any]]:
        """
        Load search index from file or create default index
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(settings.SEARCH_INDEX_PATH), exist_ok=True)
            
            index_file = f"{settings.SEARCH_INDEX_PATH}.json"
            if os.path.exists(index_file):
                with open(index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default search index
                default_index = self._create_default_index()
                with open(index_file, 'w', encoding='utf-8') as f:
                    json.dump(default_index, f, indent=2, ensure_ascii=False)
                return default_index
                
        except Exception as e:
            logging.error(f"Error loading search index: {str(e)}")
            return self._create_default_index()
    
    def _create_default_index(self) -> List[Dict[str, Any]]:
        """
        Create a default search index with sample content
        """
        return [
            {
                "id": "1",
                "title": "React Development Best Practices",
                "content": "React is a powerful JavaScript library for building user interfaces. Key best practices include component composition, proper state management, and performance optimization techniques.",
                "score": 0.0,
                "tags": ["react", "frontend", "javascript", "ui"]
            },
            {
                "id": "2",
                "title": "FastAPI Backend Development",
                "content": "FastAPI is a modern Python web framework for building APIs. It offers automatic API documentation, type checking, and high performance with async support.",
                "score": 0.0,
                "tags": ["fastapi", "python", "backend", "api"]
            },
            {
                "id": "3",
                "title": "Machine Learning Fundamentals",
                "content": "Machine learning involves training algorithms to make predictions or decisions based on data. Key concepts include supervised learning, unsupervised learning, and neural networks.",
                "score": 0.0,
                "tags": ["machine learning", "ai", "python", "data science"]
            },
            {
                "id": "4",
                "title": "Cloud Deployment Strategies",
                "content": "Cloud deployment involves hosting applications on cloud platforms like AWS, Azure, or Google Cloud. Strategies include containerization, serverless, and microservices architecture.",
                "score": 0.0,
                "tags": ["cloud", "deployment", "aws", "azure", "docker"]
            },
            {
                "id": "5",
                "title": "Web Development Architecture",
                "content": "Modern web development involves frontend frameworks, backend APIs, databases, and deployment strategies. Understanding the full stack is crucial for building scalable applications.",
                "score": 0.0,
                "tags": ["web development", "full stack", "architecture", "scalability"]
            },
            {
                "id": "6",
                "title": "API Design Principles",
                "content": "Good API design follows REST principles, includes proper error handling, versioning, and documentation. Security and performance are also key considerations.",
                "score": 0.0,
                "tags": ["api", "rest", "design", "documentation"]
            },
            {
                "id": "7",
                "title": "Database Optimization",
                "content": "Database optimization involves indexing, query optimization, and proper schema design. Performance monitoring and caching strategies are also important.",
                "score": 0.0,
                "tags": ["database", "optimization", "sql", "performance"]
            },
            {
                "id": "8",
                "title": "Frontend Framework Comparison",
                "content": "Popular frontend frameworks include React, Vue, and Angular. Each has its strengths: React for flexibility, Vue for simplicity, and Angular for enterprise applications.",
                "score": 0.0,
                "tags": ["frontend", "react", "vue", "angular", "frameworks"]
            }
        ]
    
    async def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Perform AI-powered search on the knowledge base
        """
        try:
            query_lower = query.lower()
            results = []
            
            for item in self.search_index:
                score = self._calculate_relevance_score(query_lower, item)
                if score > 0:
                    results.append({
                        "id": item["id"],
                        "title": item["title"],
                        "content": item["content"],
                        "score": score
                    })
            
            # Sort by relevance score (descending)
            results.sort(key=lambda x: x["score"], reverse=True)
            
            # Return top 10 results
            return results[:10]
            
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return []
    
    def _calculate_relevance_score(self, query: str, item: Dict[str, Any]) -> float:
        """
        Calculate relevance score using simple text matching
        In a production environment, you would use more sophisticated
        NLP techniques or vector embeddings
        """
        score = 0.0
        
        # Check title
        title_lower = item["title"].lower()
        if query in title_lower:
            score += 3.0
        elif any(word in title_lower for word in query.split()):
            score += 2.0
        
        # Check content
        content_lower = item["content"].lower()
        if query in content_lower:
            score += 2.0
        elif any(word in content_lower for word in query.split()):
            score += 1.0
        
        # Check tags
        tags = item.get("tags", [])
        for tag in tags:
            if query in tag.lower():
                score += 1.5
            elif any(word in tag.lower() for word in query.split()):
                score += 0.5
        
        # Normalize score to 0-1 range
        return min(score / 10.0, 1.0)
    
    async def get_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions based on partial query
        """
        try:
            query_lower = query.lower()
            suggestions = set()
            
            for item in self.search_index:
                title_lower = item["title"].lower()
                content_lower = item["content"].lower()
                
                # Check if query appears in title or content
                if query_lower in title_lower:
                    words = title_lower.split()
                    for i, word in enumerate(words):
                        if query_lower in word and i < len(words) - 1:
                            suggestion = " ".join(words[i:i+3])
                            if len(suggestion) > len(query):
                                suggestions.add(suggestion)
                
                if query_lower in content_lower:
                    words = content_lower.split()
                    for i, word in enumerate(words):
                        if query_lower in word and i < len(words) - 1:
                            suggestion = " ".join(words[i:i+3])
                            if len(suggestion) > len(query):
                                suggestions.add(suggestion)
            
            return list(suggestions)[:5]
            
        except Exception as e:
            logging.error(f"Suggestions error: {str(e)}")
            return []
    
    async def get_popular_searches(self) -> List[str]:
        """
        Get popular search terms
        """
        return self.popular_searches
