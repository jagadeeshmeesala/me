import React, { useState } from 'react';
import { buildApiUrl } from '../config';
import './AISearch.css';

interface SearchResult {
  answer: string;
  sources: Array<{
    title: string;
    category: string;
    url?: string;
  }>;
  confidence: number;
  query: string;
}

const AISearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(buildApiUrl('/api/search'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim(), max_results: 5 }),
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data: SearchResult = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to perform search. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#4CAF50'; // Green
    if (confidence >= 0.6) return '#FF9800'; // Orange
    return '#F44336'; // Red
  };

  const getConfidenceText = (confidence: number) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Medium Confidence';
    return 'Low Confidence';
  };

  return (
    <div className="ai-search">
      <h2>AI-Powered Search</h2>
      <p className="search-description">
        Ask me anything about my skills, experience, projects, or background. 
        I'll provide intelligent, contextual answers based on my knowledge base.
      </p>
      
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., What are your technical skills? Tell me about your projects..."
            className="search-input"
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {result && (
        <div className="search-results">
          <div className="result-header">
            <h3>Answer</h3>
            <div className="confidence-indicator">
              <span 
                className="confidence-dot" 
                style={{ backgroundColor: getConfidenceColor(result.confidence) }}
              ></span>
              <span className="confidence-text">
                {getConfidenceText(result.confidence)} ({Math.round(result.confidence * 100)}%)
              </span>
            </div>
          </div>
          
          <div className="answer-content">
            {result.answer}
          </div>

          {result.sources && result.sources.length > 0 && (
            <div className="sources-section">
              <h4>Sources:</h4>
              <div className="sources-list">
                {result.sources.map((source, index) => (
                  <div key={index} className="source-item">
                    <span className="source-title">{source.title}</span>
                    {source.category && (
                      <span className="source-category">({source.category})</span>
                    )}
                    {source.url && (
                      <a 
                        href={source.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="source-link"
                      >
                        View Source
                      </a>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="search-examples">
        <h4>Example Questions:</h4>
        <div className="example-queries">
          <button 
            onClick={() => setQuery("What are your technical skills?")}
            className="example-query"
          >
            What are your technical skills?
          </button>
          <button 
            onClick={() => setQuery("Tell me about your projects")}
            className="example-query"
          >
            Tell me about your projects
          </button>
          <button 
            onClick={() => setQuery("What's your experience with cloud computing?")}
            className="example-query"
          >
            What's your experience with cloud computing?
          </button>
          <button 
            onClick={() => setQuery("How can I contact you?")}
            className="example-query"
          >
            How can I contact you?
          </button>
        </div>
      </div>
    </div>
  );
};

export default AISearch;
