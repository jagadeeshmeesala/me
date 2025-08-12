import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from typing import Optional

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME
    
    async def send_contact_email(self, name: str, email: str, subject: str, message: str) -> bool:
        """
        Send contact form email
        """
        try:
            # For development, just log the email
            if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password]):
                logging.info(f"Contact form submission (development mode):")
                logging.info(f"From: {name} <{email}>")
                logging.info(f"Subject: {subject}")
                logging.info(f"Message: {message}")
                return True
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = self.from_email
            msg['Subject'] = f"Contact Form: {subject}"
            
            # Email body
            body = f"""
            New contact form submission:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            
            ---
            This message was sent from your personal website contact form.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logging.info(f"Contact email sent successfully from {email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send contact email: {str(e)}")
            return False
    
    async def send_notification_email(self, to_email: str, subject: str, message: str) -> bool:
        """
        Send notification email
        """
        try:
            if not all([self.smtp_host, self.smtp_port, self.smtp_user, self.smtp_password]):
                logging.info(f"Notification email (development mode):")
                logging.info(f"To: {to_email}")
                logging.info(f"Subject: {subject}")
                logging.info(f"Message: {message}")
                return True
            
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if settings.SMTP_TLS:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to send notification email: {str(e)}")
            return False
