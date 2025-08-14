#!/usr/bin/env python3
"""
Initialize RAG (Retrieval-Augmented Generation) system for personal website
"""

import os
import sys
from dotenv import load_dotenv

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.rag_service import RAGService

def main():
    """Initialize the RAG system with sample data"""
    load_dotenv()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is not set")
        print("Please set your OpenAI API key in the .env file")
        return
    
    try:
        print("🚀 Initializing RAG system...")
        
        # Initialize RAG service
        rag_service = RAGService()
        
        # Initialize with sample data
        rag_service.initialize_sample_data()
        
        print("✅ RAG system initialized successfully!")
        print("📚 Sample documents added to the knowledge base")
        
        # Test the system
        print("\n🧪 Testing RAG system...")
        
        test_queries = [
            "What are your technical skills?",
            "Tell me about your projects",
            "How can I contact you?",
            "What's your experience with cloud computing?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            result = rag_service.search_and_generate(query)
            print(f"📝 Answer: {result['answer'][:100]}...")
            print(f"🎯 Confidence: {result['confidence']:.2f}")
            print(f"📚 Sources: {len(result['sources'])} found")
        
        print("\n🎉 RAG system is ready to use!")
        print("You can now deploy your backend and test the AI search feature.")
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {str(e)}")
        return

if __name__ == "__main__":
    main()

