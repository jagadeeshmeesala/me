from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.email_service import EmailService
import logging

router = APIRouter()
email_service = EmailService()

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(BaseModel):
    message: str
    success: bool

@router.post("/contact", response_model=ContactResponse)
async def send_contact_message(request: ContactRequest):
    """
    Send contact form message
    """
    try:
        # Validate input
        if not request.name.strip():
            raise HTTPException(status_code=400, detail="Name is required")
        
        if not request.subject.strip():
            raise HTTPException(status_code=400, detail="Subject is required")
        
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Send email using the email service
        await email_service.send_contact_email(
            name=request.name.strip(),
            email=request.email,
            subject=request.subject.strip(),
            message=request.message.strip()
        )
        
        return ContactResponse(
            message="Message sent successfully! I'll get back to you soon.",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Contact form error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send message. Please try again.")

@router.get("/contact/info")
async def get_contact_info():
    """
    Get contact information
    """
    return {
        "email": "your.email@example.com",
        "phone": "+1 (555) 123-4567",
        "location": "San Francisco, CA",
        "social_links": {
            "linkedin": "https://linkedin.com/in/your-profile",
            "github": "https://github.com/yourusername",
            "twitter": "https://twitter.com/yourusername"
        }
    }
