# 🚀 Google Cloud Platform Deployment Guide

This guide will help you deploy your personal website to Google Cloud Platform using Cloud Run.

## 📋 Prerequisites

### 1. Google Cloud Account
- Create a Google Cloud account at [cloud.google.com](https://cloud.google.com)
- Enable billing for your project

### 2. Google Cloud CLI
Install the Google Cloud CLI:

**macOS (using Homebrew):**
```bash
brew install google-cloud-sdk
```

**Windows:**
Download from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 3. Project Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Note your **Project ID** (you'll need this for deployment)

## 🔧 Pre-Deployment Setup

### 1. Update Project ID
Edit the deployment script:
```bash
cd personal-website
nano deploy-google-cloud.sh
```

Change this line:
```bash
PROJECT_ID="your-project-id"  # Replace with your actual Google Cloud Project ID
```

### 2. Update LinkedIn URL
Edit the Header component to include your actual LinkedIn URL:
```bash
nano frontend/src/components/Header.tsx
```

Update the LinkedIn link:
```jsx
<a href="https://linkedin.com/in/YOUR_USERNAME" target="_blank" rel="noopener noreferrer">
```

### 3. Add Your Profile Photo
Place your profile photo in the frontend public directory:
```bash
cp /path/to/your/photo.jpg frontend/public/profile-photo.jpg
```

## 🚀 Deployment Steps

### 1. Authenticate with Google Cloud
```bash
gcloud auth login
gcloud auth application-default login
```

### 2. Set Your Project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### 3. Run the Deployment Script
```bash
chmod +x deploy-google-cloud.sh
./deploy-google-cloud.sh
```

## 📊 What the Script Does

1. **Enables Required APIs:**
   - Cloud Run API
   - Cloud Build API
   - Container Registry API

2. **Deploys Backend:**
   - Builds Python FastAPI application
   - Deploys to Cloud Run
   - Sets environment variables
   - Configures memory and CPU

3. **Deploys Frontend:**
   - Builds React application
   - Configures Nginx with backend proxy
   - Deploys to Cloud Run
   - Sets up security headers

4. **Provides URLs:**
   - Frontend URL (your main website)
   - Backend URL (API endpoint)

## 🔧 Post-Deployment Configuration

### 1. Environment Variables
Update backend environment variables:
```bash
gcloud run services update personal-website-backend \
  --region=us-central1 \
  --set-env-vars "SECRET_KEY=your-secret-key,DATABASE_URL=sqlite:///./data/app.db"
```

### 2. Custom Domain (Optional)
1. Go to Cloud Run in Google Cloud Console
2. Select your frontend service
3. Click "Manage Custom Domains"
4. Add your domain and configure DNS

### 3. SSL Certificate
Cloud Run automatically provides SSL certificates for custom domains.

## 📈 Monitoring and Logs

### View Logs
```bash
# Frontend logs
gcloud logs tail --service=personal-website-frontend --region=us-central1

# Backend logs
gcloud logs tail --service=personal-website-backend --region=us-central1
```

### Monitor Performance
- Go to Google Cloud Console
- Navigate to Cloud Run
- View metrics, logs, and performance data

## 🔄 Updating Your Website

### 1. Code Changes
Make your changes locally, then redeploy:
```bash
./deploy-google-cloud.sh
```

### 2. Environment Variables
Update environment variables:
```bash
gcloud run services update personal-website-backend \
  --region=us-central1 \
  --set-env-vars "NEW_VAR=value"
```

### 3. Scaling
Adjust resources if needed:
```bash
gcloud run services update personal-website-frontend \
  --region=us-central1 \
  --memory=1Gi \
  --cpu=2 \
  --max-instances=20
```

## 💰 Cost Optimization

### Free Tier
- Cloud Run offers a generous free tier
- 2 million requests per month
- 360,000 vCPU-seconds
- 180,000 GiB-seconds of memory

### Cost Monitoring
- Set up billing alerts in Google Cloud Console
- Monitor usage in the Billing section
- Use Cloud Monitoring for resource optimization

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit sensitive data to version control
- Use Google Cloud Secret Manager for secrets
- Rotate keys regularly

### 2. CORS Configuration
Update CORS settings in your backend:
```python
# In app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Security Headers
The deployment script includes security headers in Nginx configuration.

## 🆘 Troubleshooting

### Common Issues

1. **Authentication Error:**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Project Not Found:**
   ```bash
   gcloud projects list
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **API Not Enabled:**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

4. **Build Failures:**
   - Check logs: `gcloud logs tail --service=service-name --region=us-central1`
   - Verify Dockerfile syntax
   - Check for missing dependencies

### Getting Help
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Cloud Support](https://cloud.google.com/support)

## 🎉 Success!

Your personal website is now deployed on Google Cloud Platform! 

**Next Steps:**
1. Test all functionality (AI search, contact form, etc.)
2. Set up monitoring and alerts
3. Configure custom domain if needed
4. Share your website URL

**Your website will be available at:**
- Frontend: `https://personal-website-frontend-xxxxx-uc.a.run.app`
- Backend: `https://personal-website-backend-xxxxx-uc.a.run.app`
