import React from 'react';
import HeaderVisitorCounter from './HeaderVisitorCounter';
import './Header.css';

interface HeaderProps {
  currentSection: string;
  setCurrentSection: (section: string) => void;
}

const Header: React.FC<HeaderProps> = ({ currentSection, setCurrentSection }) => {
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'about', label: 'About' },
    { id: 'projects', label: 'Projects' },
    { id: 'ai-search', label: 'AI Search' },
    { id: 'contact', label: 'Contact' }
  ];

  return (
    <header className="header">
      <div className="container">
        {/* Visitor Counter Banner */}
        <div className="visitor-banner">
          <HeaderVisitorCounter />
        </div>
        
        <div className="header-content">
          <div className="logo">
            <h2>Jagadeesh Meesala</h2>
          </div>
          
          <nav className="nav">
            <ul className="nav-list">
              {navItems.map((item) => (
                <li key={item.id}>
                  <button
                    className={`nav-link ${currentSection === item.id ? 'active' : ''}`}
                    onClick={() => setCurrentSection(item.id)}
                  >
                    {item.label}
                  </button>
                </li>
              ))}
            </ul>
          </nav>
          
          <div className="social-links">
            <a
              href="https://linkedin.com/in/jagadeeshmeesala"
              target="_blank"
              rel="noopener noreferrer"
              className="social-link linkedin"
            >
              <i className="fab fa-linkedin"></i>
            </a>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
