import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
import chromadb
import hashlib
from datetime import datetime

class RAGService:
    def __init__(self):
        self.openai_client = None
        self.chroma_client = chromadb.PersistentClient(path="./data/chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="personal_website_docs",
            metadata={"description": "Personal website documents for RAG"}
        )
    
    def _get_openai_client(self):
        """Get OpenAI client, initializing it if needed"""
        if self.openai_client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")
            self.openai_client = OpenAI(api_key=api_key)
        return self.openai_client
               
    def add_document(self, content: str, metadata: Dict[str, Any], doc_id: Optional[str] = None) -> str:
        """Add a document to the vector database"""
        if not doc_id:
            doc_id = hashlib.md5(content.encode()).hexdigest()
        
        # Generate embedding
        embedding = self._get_embedding(content)
        
        # Add to collection
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def search_and_generate(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search for relevant documents and generate a response"""
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            if not results['documents'][0]:
                return {
                    "answer": "I don't have specific information about that. Could you please rephrase your question or ask about my skills, projects, or experience?",
                    "sources": [],
                    "confidence": 0.0
                }
            
            # Prepare context for LLM
            context = self._prepare_context(results['documents'][0], results['metadatas'][0])
            
            # Generate response using OpenAI
            response = self._generate_response(query, context)
            
            return {
                "answer": response,
                "sources": results['metadatas'][0],
                "confidence": self._calculate_confidence(results['distances'][0])
            }
        except Exception as e:
            return {
                "answer": f"Sorry, I encountered an error while processing your request: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
    
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI"""
        client = self._get_openai_client()
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    
    def _prepare_context(self, documents: List[str], metadatas: List[Dict]) -> str:
        """Prepare context from retrieved documents"""
        context_parts = []
        for i, (doc, metadata) in enumerate(zip(documents, metadatas)):
            source_info = f"Source {i+1}: {metadata.get('title', 'Unknown')}"
            if metadata.get('url'):
                source_info += f" ({metadata.get('url')})"
            context_parts.append(f"{source_info}\n{doc}\n")
        
        return "\n".join(context_parts)
    
    def _generate_response(self, query: str, context: str) -> str:
        """Generate response using OpenAI GPT"""
        client = self._get_openai_client()
        system_prompt = """You are Jagadeesh Meesala's AI assistant. You help answer questions about Jagadeesh's skills, experience, projects, and background. 
        
        Use the provided context to answer questions accurately and helpfully. If the context doesn't contain relevant information, politely say so and suggest asking about other topics.
        
        Always be professional, friendly, and accurate. If you're not sure about something, say so rather than making things up."""
        
        user_prompt = f"""Context information:
{context}

Question: {query}

Please provide a helpful and accurate answer based on the context above."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _calculate_confidence(self, distances: List[float]) -> float:
        """Calculate confidence based on similarity distances"""
        if not distances:
            return 0.0
        
        # Convert distances to similarities (1 - normalized_distance)
        similarities = [1 - (d / max(distances)) for d in distances]
        return sum(similarities) / len(similarities)
    
    def initialize_sample_data(self):
        """Initialize the database with sample documents about Jagadeesh"""
        sample_docs = [
            {
                "content": """Jagadeesh Meesala is a software engineer with expertise in full-stack development, cloud computing, and AI/ML technologies. 
                He has experience with React, TypeScript, Python, FastAPI, and Google Cloud Platform. 
                Jagadeesh specializes in building scalable web applications and has worked on projects involving machine learning and data analysis.""",
                "metadata": {
                    "title": "Professional Background",
                    "category": "experience",
                    "url": "https://jagadeeshmeesala.app/about"
                }
            },
            {
                "content": """Technical Skills: React, TypeScript, Python, FastAPI, Node.js, Google Cloud Platform, AWS, Docker, Kubernetes, 
                Machine Learning, Data Analysis, SQL, MongoDB, PostgreSQL, Git, CI/CD, REST APIs, GraphQL, 
                Microservices Architecture, Serverless Computing, and DevOps practices.""",
                "metadata": {
                    "title": "Technical Skills",
                    "category": "skills",
                    "url": "https://jagadeeshmeesala.app/skills"
                }
            },
            {
                "content": """Jagadeesh has worked on various projects including this personal website built with React frontend and FastAPI backend, 
                deployed on Google Cloud Run with custom domain configuration. He has experience in AI/ML projects, 
                web application development, and cloud infrastructure management.""",
                "metadata": {
                    "title": "Projects",
                    "category": "projects",
                    "url": "https://jagadeeshmeesala.app/projects"
                }
            },
            {
                "content": """Jagadeesh is based in Baltimore, MD and is available for freelance work, consulting, and full-time opportunities. 
                He can be contacted through the contact form on his website or via email at jagadeesh.hya@gmail.com. 
                He specializes in modern web development, cloud solutions, and AI integration.""",
                "metadata": {
                    "title": "Contact Information",
                    "category": "contact",
                    "url": "https://jagadeeshmeesala.app/contact"
                }
            }
        ]
        
        for doc in sample_docs:
            self.add_document(doc["content"], doc["metadata"])
        
        print(f"Initialized RAG service with {len(sample_docs)} sample documents")
