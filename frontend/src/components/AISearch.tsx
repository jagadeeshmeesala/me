import React, { useState } from 'react';
import './AISearch.css';

interface SearchResult {
  id: string;
  title: string;
  content: string;
  score: number;
}

const AISearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      if (!response.ok) {
        throw new Error('Search request failed');
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError('Failed to perform search. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="ai-search section">
      <div className="search-container">
        <h2 className="section-title">AI-Powered Search</h2>
        <p className="section-subtitle">
          Search through my knowledge base using advanced AI algorithms
        </p>

        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask me anything..."
              className="search-input"
              disabled={loading}
            />
            <button type="submit" className="search-btn" disabled={loading}>
              {loading ? (
                <i className="fas fa-spinner fa-spin"></i>
              ) : (
                <i className="fas fa-search"></i>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <i className="fas fa-exclamation-triangle"></i>
            {error}
          </div>
        )}

        {results.length > 0 && (
          <div className="search-results">
            <h3>Search Results ({results.length})</h3>
            <div className="results-list">
              {results.map((result) => (
                <div key={result.id} className="result-card">
                  <h4 className="result-title">{result.title}</h4>
                  <p className="result-content">{result.content}</p>
                  <div className="result-meta">
                    <span className="result-score">
                      Relevance: {Math.round(result.score * 100)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {!loading && !error && results.length === 0 && query && (
          <div className="no-results">
            <i className="fas fa-search"></i>
            <p>No results found for "{query}"</p>
            <p>Try different keywords or rephrase your query.</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default AISearch;
