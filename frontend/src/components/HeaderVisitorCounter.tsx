import React, { useState, useEffect } from 'react';
import { buildApiUrl } from '../config';
import './HeaderVisitorCounter.css';

interface VisitorStats {
  total_visitors: number;
  unique_visitors: number;
  today_visitors: number;
}

const HeaderVisitorCounter: React.FC = () => {
  const [stats, setStats] = useState<VisitorStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Track this visit when component mounts
    trackVisit();
    
    // Get current visitor stats
    fetchVisitorStats();
    
    // Set up interval to refresh stats every 30 seconds
    const interval = setInterval(fetchVisitorStats, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const trackVisit = async () => {
    try {
      await fetch(buildApiUrl('/api/analytics/track-visit'), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          page: window.location.pathname,
          user_agent: navigator.userAgent
        }),
      });
    } catch (err) {
      console.error('Failed to track visit:', err);
    }
  };

  const fetchVisitorStats = async () => {
    try {
      const response = await fetch(buildApiUrl('/api/analytics/visitor-count'));
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      } else {
        throw new Error('Failed to fetch visitor stats');
      }
    } catch (err) {
      setError('Failed to load visitor statistics');
      console.error('Error fetching visitor stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  if (loading) {
    return (
      <div className="header-visitor-counter loading">
        <span className="counter-text">Loading visitors...</span>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="header-visitor-counter error">
        <span className="counter-icon">👥</span>
        <span className="counter-text">Visitors</span>
      </div>
    );
  }

  return (
    <div className="header-visitor-counter">
      <div className="counter-item">
        <span className="counter-icon">👥</span>
        <div className="counter-details">
          <span className="counter-number">{formatNumber(stats.total_visitors)}</span>
          <span className="counter-label">Total</span>
        </div>
      </div>
      
      <div className="counter-item">
        <span className="counter-icon">🆕</span>
        <div className="counter-details">
          <span className="counter-number">{formatNumber(stats.unique_visitors)}</span>
          <span className="counter-label">Unique</span>
        </div>
      </div>
      
      <div className="counter-item today">
        <span className="counter-icon">📅</span>
        <div className="counter-details">
          <span className="counter-number">{formatNumber(stats.today_visitors)}</span>
          <span className="counter-label">Today</span>
        </div>
      </div>
    </div>
  );
};

export default HeaderVisitorCounter;

