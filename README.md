# Personal Website

A modern, responsive personal website built with React frontend and FastAPI backend, featuring AI-powered search functionality and cloud deployment capabilities.

## 🌟 Features

### Frontend (React + TypeScript)
- **Modern UI/UX**: Beautiful, responsive design with glassmorphism effects
- **LinkedIn Integration**: Direct link to your LinkedIn profile
- **AI Search**: Intelligent search functionality powered by the backend
- **Portfolio Showcase**: Display your projects with modern card layouts
- **Contact Form**: Functional contact form with email integration
- **Responsive Design**: Works perfectly on all devices
- **Smooth Animations**: Engaging user interactions and transitions

### Backend (FastAPI + Python)
- **RESTful API**: Clean, documented API endpoints
- **AI Search Engine**: Intelligent search with relevance scoring
- **Contact Form Processing**: Email integration for contact submissions
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Docker Support**: Containerized deployment ready
- **Cloud Ready**: Optimized for Google Cloud and Azure deployment

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd personal-website
   ```

2. **Start the Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python run.py
   ```
   The backend will be available at `http://localhost:8000`

3. **Start the Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

### Using Docker Compose
```bash
docker-compose up --build
```

## 🏗️ Project Structure

```
personal-website/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx         # Main app component
│   │   └── index.tsx       # Entry point
│   ├── public/             # Static assets
│   ├── package.json        # Frontend dependencies
│   └── Dockerfile          # Frontend container
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── docker-compose.yml      # Local development
├── deploy-google-cloud.sh  # Google Cloud deployment
├── deploy-azure.sh         # Azure deployment
└── README.md              # This file
```

## 🔧 Configuration

### Frontend Configuration
Update the following in `frontend/src/components/Header.tsx`:
- Your name in the logo section
- LinkedIn profile URL
- Other social media links

Update project information in `frontend/src/components/Projects.tsx`:
- Project details
- GitHub repository links
- Live demo URLs

### Backend Configuration
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./data/app.db
SMTP_HOST=your-smtp-host
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=your-email-password
EMAILS_FROM_EMAIL=your-email@example.com
EMAILS_FROM_NAME=Your Name
```

## 🌐 Deployment

### Google Cloud Platform
1. Install Google Cloud CLI
2. Update `PROJECT_ID` in `deploy-google-cloud.sh`
3. Run the deployment script:
   ```bash
   chmod +x deploy-google-cloud.sh
   ./deploy-google-cloud.sh
   ```

### Microsoft Azure
1. Install Azure CLI
2. Update configuration variables in `deploy-azure.sh`
3. Run the deployment script:
   ```bash
   chmod +x deploy-azure.sh
   ./deploy-azure.sh
   ```

### Manual Deployment
1. **Build Frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🔍 AI Search Features

The AI search functionality includes:
- **Semantic Search**: Intelligent content matching
- **Relevance Scoring**: Results ranked by relevance
- **Search Suggestions**: Auto-complete functionality
- **Popular Searches**: Trending search terms
- **Extensible Index**: Easy to add new content

### Adding Content to Search Index
Update the search index in `backend/app/services/search_service.py`:
```python
def _create_default_index(self) -> List[Dict[str, Any]]:
    return [
        {
            "id": "unique-id",
            "title": "Your Content Title",
            "content": "Your content description...",
            "score": 0.0,
            "tags": ["tag1", "tag2", "tag3"]
        }
    ]
```

## 📧 Contact Form

The contact form supports:
- Email validation
- Spam protection
- SMTP integration
- Development mode logging

### Email Configuration
Configure your email settings in the backend `.env` file:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 🛠️ Customization

### Styling
- Update colors in `frontend/src/App.css`
- Modify component styles in individual CSS files
- Change the gradient background in `frontend/src/index.css`

### Content
- Update personal information in components
- Add/remove sections as needed
- Customize project showcase
- Modify skills and experience

### API Endpoints
- Add new endpoints in `backend/app/api/routes/`
- Extend search functionality
- Add authentication if needed

## 🔒 Security Considerations

- Update `SECRET_KEY` in production
- Configure CORS origins properly
- Use HTTPS in production
- Implement rate limiting
- Add input validation
- Consider adding authentication for admin features

## 📊 Performance Optimization

- Frontend assets are optimized with webpack
- Backend uses async/await for better performance
- Static file caching configured
- Gzip compression enabled
- Database connection pooling (when using databases)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🎯 Roadmap

- [ ] Add blog functionality
- [ ] Implement user authentication
- [ ] Add analytics dashboard
- [ ] Create admin panel
- [ ] Add more AI features
- [ ] Implement caching layer
- [ ] Add database integration
- [ ] Create mobile app

---

**Built with ❤️ using React, TypeScript, FastAPI, and Python**
