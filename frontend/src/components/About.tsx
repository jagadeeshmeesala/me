import React from 'react';
import './About.css';

const About: React.FC = () => {
  const skills = [
    { name: 'React', level: 90 },
    { name: 'TypeScript', level: 85 },
    { name: 'Python', level: 90 },
    { name: 'FastAPI', level: 85 },
    { name: 'Node.js', level: 80 },
    { name: 'AWS/Azure', level: 75 },
    { name: 'Docker', level: 80 },
    { name: 'Machine Learning', level: 70 }
  ];

  return (
    <section className="about section">
      <div className="about-container">
        <h2 className="section-title">About Me</h2>
        <p className="section-subtitle">
          Passionate developer with expertise in modern web technologies and AI
        </p>

        <div className="about-content">
          <div className="about-text">
            <div className="card">
              <h3>Who I Am</h3>
              <p>
                I'm a full-stack developer with over 15 years of experience building 
                scalable web applications. I specialize in React, TypeScript, Python, 
                and modern cloud technologies. My passion lies in creating intuitive 
                user experiences and implementing cutting-edge AI solutions.
              </p>
            </div>

            <div className="card">
              <h3>What I Do</h3>
              <p>
                I develop end-to-end solutions from concept to deployment, focusing on 
                performance, scalability, and user experience. I work with modern 
                frameworks and cloud platforms to deliver robust applications that 
                solve real-world problems.
              </p>
            </div>

            <div className="card">
              <h3>My Approach</h3>
              <p>
                I believe in clean, maintainable code and user-centered design. 
                Every project I work on is an opportunity to learn and innovate. 
                I stay updated with the latest technologies and best practices to 
                deliver exceptional results.
              </p>
            </div>
          </div>

          <div className="skills-section">
            <h3>Technical Skills</h3>
            <div className="skills-grid">
              {skills.map((skill) => (
                <div key={skill.name} className="skill-item">
                  <div className="skill-header">
                    <span className="skill-name">{skill.name}</span>
                    <span className="skill-level">{skill.level}%</span>
                  </div>
                  <div className="skill-bar">
                    <div 
                      className="skill-progress" 
                      style={{ width: `${skill.level}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
