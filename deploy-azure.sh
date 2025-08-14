#!/bin/bash

# Microsoft Azure Deployment Script
# This script deploys the personal website to Azure Container Instances

set -e

# Configuration
RESOURCE_GROUP="personal-website-rg"
LOCATION="eastus"
FRONTEND_APP_NAME="personal-website-frontend"
BACKEND_APP_NAME="personal-website-backend"
ACR_NAME="personalwebsiteacr"

echo "🚀 Starting Azure deployment..."

# Check if az CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    exit 1
fi

# Login to Azure
echo "🔐 Logging into Azure..."
az login

# Create resource group
echo "📋 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
echo "🏗️ Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
az acr update -n $ACR_NAME --admin-enabled true

# Get ACR credentials
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" --output tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)

# Build and push backend image
echo "🏗️ Building and pushing backend image..."
cd backend
az acr build --registry $ACR_NAME --image backend:latest .

# Build and push frontend image
echo "🏗️ Building and pushing frontend image..."
cd ../frontend
az acr build --registry $ACR_NAME --image frontend:latest .

# Deploy backend to Container Instances
echo "🚀 Deploying backend..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP_NAME \
    --image $ACR_LOGIN_SERVER/backend:latest \
    --dns-name-label $BACKEND_APP_NAME \
    --ports 8000 \
    --registry-login-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD \
    --environment-variables \
        DATABASE_URL="sqlite:///./data/app.db" \
        SECRET_KEY="your-secret-key-here"

# Get backend URL
BACKEND_URL="http://$BACKEND_APP_NAME.$LOCATION.azurecontainer.io:8000"
echo "✅ Backend deployed at: $BACKEND_URL"

# Update nginx config with backend URL
sed -i "s|http://backend:8000|$BACKEND_URL|g" nginx.conf

# Rebuild frontend with updated config
az acr build --registry $ACR_NAME --image frontend:latest .

# Deploy frontend to Container Instances
echo "🚀 Deploying frontend..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $FRONTEND_APP_NAME \
    --image $ACR_LOGIN_SERVER/frontend:latest \
    --dns-name-label $FRONTEND_APP_NAME \
    --ports 80 \
    --registry-login-server $ACR_LOGIN_SERVER \
    --registry-username $ACR_USERNAME \
    --registry-password $ACR_PASSWORD

# Get frontend URL
FRONTEND_URL="http://$FRONTEND_APP_NAME.$LOCATION.azurecontainer.io"
echo "✅ Frontend deployed at: $FRONTEND_URL"

echo "🎉 Deployment completed successfully!"
echo "🌐 Frontend: $FRONTEND_URL"
echo "🔧 Backend: $BACKEND_URL"
echo ""
echo "📝 Next steps:"
echo "1. Update your LinkedIn profile URL in the frontend code"
echo "2. Configure environment variables in Azure Portal"
echo "3. Set up a custom domain if needed"
echo "4. Consider using Azure App Service for better scalability"
