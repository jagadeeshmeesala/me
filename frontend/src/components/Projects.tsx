import React from 'react';
import './Projects.css';

interface Project {
  id: string;
  title: string;
  description: string;
  technologies: string[];
  image: string;
  github?: string;
  live?: string;
}

const Projects: React.FC = () => {
  const projects: Project[] = [
    {
      id: '1',
      title: 'E-Commerce Platform',
      description: 'A full-stack e-commerce solution with React frontend and FastAPI backend, featuring user authentication, payment processing, and admin dashboard.',
      technologies: ['React', 'TypeScript', 'FastAPI', 'PostgreSQL', 'Stripe'],
      image: '🛒',
      github: 'https://github.com/yourusername/ecommerce-platform',
      live: 'https://ecommerce-demo.com'
    },
    {
      id: '2',
      title: 'AI Chat Assistant',
      description: 'An intelligent chatbot powered by machine learning algorithms, capable of understanding context and providing helpful responses.',
      technologies: ['Python', 'TensorFlow', 'React', 'FastAPI', 'Redis'],
      image: '🤖',
      github: 'https://github.com/yourusername/ai-chat-assistant'
    },
    {
      id: '3',
      title: 'Task Management App',
      description: 'A collaborative task management application with real-time updates, team collaboration features, and progress tracking.',
      technologies: ['React', 'Node.js', 'Socket.io', 'MongoDB', 'Express'],
      image: '📋',
      github: 'https://github.com/yourusername/task-manager',
      live: 'https://task-manager-demo.com'
    },
    {
      id: '4',
      title: 'Weather Dashboard',
      description: 'A beautiful weather application with location-based forecasts, interactive maps, and detailed weather analytics.',
      technologies: ['React', 'TypeScript', 'OpenWeather API', 'Chart.js', 'CSS3'],
      image: '🌤️',
      github: 'https://github.com/yourusername/weather-dashboard',
      live: 'https://weather-demo.com'
    }
  ];

  return (
    <section className="projects section">
      <div className="projects-container">
        <h2 className="section-title">My Projects</h2>
        <p className="section-subtitle">
          Here are some of the projects I've worked on recently
        </p>

        {/* <div className="projects-grid">
          {projects.map((project) => (
            <div key={project.id} className="project-card">
              <div className="project-image">
                <span className="project-emoji">{project.image}</span>
              </div>
              
              <div className="project-content">
                <h3 className="project-title">{project.title}</h3>
                <p className="project-description">{project.description}</p>
                
                <div className="project-technologies">
                  {project.technologies.map((tech) => (
                    <span key={tech} className="tech-tag">
                      {tech}
                    </span>
                  ))}
                </div>
                
                <div className="project-links">
                  {project.github && (
                    <a 
                      href={project.github} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="project-link github"
                    >
                      <i className="fab fa-github"></i>
                      GitHub
                    </a>
                  )}
                  {project.live && (
                    <a 
                      href={project.live} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="project-link live"
                    >
                      <i className="fas fa-external-link-alt"></i>
                      Live Demo
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div> */}
      </div>
    </section>
  );
};

export default Projects;
