#!/bin/bash

# Google Cloud Platform Deployment Script
# This script deploys the personal website to Google Cloud Run

set -e

# Configuration - UPDATE THESE VALUES
PROJECT_ID="personal-website-468806"  # Replace with your actual Google Cloud Project ID
REGION="us-central1"
FRONTEND_SERVICE_NAME="personal-website-frontend"
BACKEND_SERVICE_NAME="personal-website-backend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Google Cloud deployment...${NC}"

# Check if PROJECT_ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo -e "${RED}❌ Please update PROJECT_ID in this script with your actual Google Cloud Project ID${NC}"
    echo -e "${YELLOW}💡 You can find your Project ID in the Google Cloud Console${NC}"
    exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first:${NC}"
    echo -e "${YELLOW}   https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}🔐 Please authenticate with Google Cloud:${NC}"
    gcloud auth login
fi

# Set the project
echo -e "${BLUE}📋 Setting project to $PROJECT_ID...${NC}"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create .env file for backend if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}📝 Creating backend environment file...${NC}"
    cat > backend/.env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./data/app.db

# Security
SECRET_KEY=$(openssl rand -hex 32)

# API Configuration
API_V1_STR=/api
PROJECT_NAME=Personal Website API

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://your-frontend-domain.com"]

# Email Settings (optional)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# AI Search Settings
AI_SEARCH_ENABLED=True
SEARCH_INDEX_PATH=./data/search_index.json
EOF
    echo -e "${GREEN}✅ Backend .env file created${NC}"
fi

# Build and deploy backend
echo -e "${BLUE}🏗️ Building and deploying backend...${NC}"
cd backend

# Create a temporary Dockerfile for Cloud Run
cat > Dockerfile.cloudrun << EOF
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

gcloud run deploy $BACKEND_SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8000 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars "DATABASE_URL=sqlite:///./data/app.db,SECRET_KEY=$(openssl rand -hex 32)" \
    --timeout 300

# Clean up temporary Dockerfile
rm Dockerfile.cloudrun

# Get backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --region=$REGION --format='value(status.url)')
echo -e "${GREEN}✅ Backend deployed at: $BACKEND_URL${NC}"

# Build and deploy frontend
echo -e "${BLUE}🏗️ Building and deploying frontend...${NC}"
cd ../frontend

# Create a temporary nginx config with the backend URL
cat > nginx.cloudrun.conf << EOF
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;

    # Handle React Router
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass $BACKEND_URL;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Create a temporary Dockerfile for Cloud Run
cat > Dockerfile.cloudrun << EOF
# Build stage
FROM node:16-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.cloudrun.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
EOF

gcloud run deploy $FRONTEND_SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 80 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --timeout 300

# Clean up temporary files
rm Dockerfile.cloudrun nginx.cloudrun.conf

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE_NAME --region=$REGION --format='value(status.url)')
echo -e "${GREEN}✅ Frontend deployed at: $FRONTEND_URL${NC}"

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${BLUE}🌐 Frontend: $FRONTEND_URL${NC}"
echo -e "${BLUE}🔧 Backend: $BACKEND_URL${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Update your LinkedIn profile URL in the frontend code"
echo "2. Configure environment variables in Google Cloud Console"
echo "3. Set up a custom domain if needed"
echo "4. Test the AI search functionality"
echo ""
echo -e "${YELLOW}🔧 To update environment variables:${NC}"
echo "gcloud run services update $BACKEND_SERVICE_NAME --region=$REGION --set-env-vars KEY=VALUE"
echo ""
echo -e "${YELLOW}📊 To view logs:${NC}"
echo "gcloud logs tail --service=$FRONTEND_SERVICE_NAME --region=$REGION"
echo "gcloud logs tail --service=$BACKEND_SERVICE_NAME --region=$REGION"
