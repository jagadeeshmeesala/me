import React from 'react';
import './Hero.css';

const Hero: React.FC = () => {
  return (
    <section className="hero section">
      <div className="hero-content">
        <div className="hero-badge">
          <span>🚀 Available for opportunities</span>
        </div>
        
        <h1 className="hero-title">
          Crafting Digital <span className="highlight">Experiences</span> That Matter
        </h1>
        
        <p className="hero-subtitle">
          I'm <strong>Jagadeesh Meesala</strong>, a passionate Full Stack Developer
        </p>
        
        <p className="hero-description">
          Transforming ideas into elegant, scalable solutions. Specializing in modern web technologies, 
          AI integration, and creating seamless user experiences that drive business growth.
        </p>
        
        <div className="hero-buttons">
          <button className="btn">Explore My Work</button>
          <button className="btn btn-secondary">Let's Connect</button>
        </div>
        
        <div className="hero-stats">
          <div className="stat">
            <h3>15+</h3>
            <p>Years Experience</p>
          </div>
          {/* <div className="stat">
            <h3>50+</h3>
            <p>Projects Delivered</p>
          </div> */}
          <div className="stat">
            <h3>100%</h3>
            <p>Client Success</p>
          </div>
        </div>
        
        <div className="hero-tech">
          <span className="tech-label">Tech Stack:</span>
          <div className="tech-icons">
            <span className="tech-icon">React</span>
            <span className="tech-icon">Python</span>
            <span className="tech-icon">FastAPI</span>
            <span className="tech-icon">AI/ML</span>
          </div>
        </div>
      </div>
      
      <div className="hero-image">
        <div className="profile-image">
          <img 
            src="/profile-photo.jpg" 
            alt="Jagadeesh Meesala" 
            className="profile-photo"
          />
        </div>
      </div>
    </section>
  );
};

export default Hero;
