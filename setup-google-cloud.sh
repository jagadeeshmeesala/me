#!/bin/bash

# Google Cloud Setup Script
# This script helps you set up Google Cloud for deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Google Cloud Setup Script${NC}"
echo "This script will help you set up Google Cloud for deployment."
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed.${NC}"
    echo -e "${YELLOW}Please install it first:${NC}"
    echo ""
    echo "macOS (using Homebrew):"
    echo "  brew install google-cloud-sdk"
    echo ""
    echo "Windows:"
    echo "  Download from https://cloud.google.com/sdk/docs/install"
    echo ""
    echo "Linux:"
    echo "  curl https://sdk.cloud.google.com | bash"
    echo "  exec -l \$SHELL"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ gcloud CLI is installed${NC}"

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${YELLOW}🔐 You need to authenticate with Google Cloud${NC}"
    echo "This will open your browser for authentication..."
    gcloud auth login
else
    echo -e "${GREEN}✅ Already authenticated with Google Cloud${NC}"
fi

# List available projects
echo ""
echo -e "${BLUE}📋 Available projects:${NC}"
gcloud projects list --format="table(projectId,name,projectNumber)"

echo ""
echo -e "${YELLOW}💡 To create a new project:${NC}"
echo "1. Go to https://console.cloud.google.com"
echo "2. Click 'Select a project' > 'New Project'"
echo "3. Enter a project name and click 'Create'"
echo "4. Note the Project ID (you'll need it for deployment)"
echo ""

# Ask for project ID
read -p "Enter your Google Cloud Project ID: " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Project ID is required${NC}"
    exit 1
fi

# Set the project
echo -e "${BLUE}📋 Setting project to $PROJECT_ID...${NC}"
gcloud config set project $PROJECT_ID

# Enable billing check
echo -e "${BLUE}💰 Checking billing status...${NC}"
BILLING_ACCOUNT=$(gcloud billing projects describe $PROJECT_ID --format="value(billingAccountName)" 2>/dev/null || echo "")

if [ -z "$BILLING_ACCOUNT" ]; then
    echo -e "${YELLOW}⚠️  Billing is not enabled for this project${NC}"
    echo "You need to enable billing to use Cloud Run:"
    echo "1. Go to https://console.cloud.google.com/billing"
    echo "2. Select your project"
    echo "3. Click 'Link a billing account'"
    echo "4. Create a new billing account or link an existing one"
    echo ""
    echo -e "${YELLOW}Note: Cloud Run has a generous free tier${NC}"
else
    echo -e "${GREEN}✅ Billing is enabled${NC}"
fi

# Enable required APIs
echo -e "${BLUE}🔧 Enabling required APIs...${NC}"
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo -e "${GREEN}✅ APIs enabled successfully${NC}"

# Update deployment script
echo -e "${BLUE}📝 Updating deployment script...${NC}"
sed -i.bak "s/PROJECT_ID=\"your-project-id\"/PROJECT_ID=\"$PROJECT_ID\"/" deploy-google-cloud.sh
rm deploy-google-cloud.sh.bak

echo -e "${GREEN}✅ Deployment script updated with your Project ID${NC}"

echo ""
echo -e "${GREEN}🎉 Google Cloud setup completed!${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Update your LinkedIn URL in frontend/src/components/Header.tsx"
echo "2. Add your profile photo to frontend/public/profile-photo.jpg"
echo "3. Run the deployment: ./deploy-google-cloud.sh"
echo ""
echo -e "${BLUE}🔗 Useful links:${NC}"
echo "- Google Cloud Console: https://console.cloud.google.com"
echo "- Cloud Run Documentation: https://cloud.google.com/run/docs"
echo "- Billing: https://console.cloud.google.com/billing"
