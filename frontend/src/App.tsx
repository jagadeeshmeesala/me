import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import Projects from './components/Projects';
import Contact from './components/Contact';
import AISearch from './components/AISearch';
import './App.css';

const App: React.FC = () => {
  const [currentSection, setCurrentSection] = useState('home');

  const renderSection = () => {
    switch (currentSection) {
      case 'home':
        return <Hero />;
      case 'about':
        return <About />;
      case 'projects':
        return <Projects />;
      case 'ai-search':
        return <AISearch />;
      case 'contact':
        return <Contact />;
      default:
        return <Hero />;
    }
  };

  return (
    <div className="App">
      <Header currentSection={currentSection} setCurrentSection={setCurrentSection} />
      <main className="main-content">
        {renderSection()}
      </main>
    </div>
  );
};

export default App;
