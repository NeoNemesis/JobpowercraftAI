"""
Email automation module for sending job applications with generated resumes and cover letters.
"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from loguru import logger


class EmailSender:
    """Handles automated email sending for job applications."""
    
    def __init__(self, email_config_path: Path):
        """
        Initialize EmailSender with configuration.
        
        Args:
            email_config_path: Path to email configuration YAML file
        """
        self.config = self._load_email_config(email_config_path)
        self.smtp_server = None
        
    def _load_email_config(self, config_path: Path) -> Dict:
        """Load email configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                
            required_fields = ['smtp_server', 'smtp_port', 'email', 'password', 'sender_name']
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field '{field}' in email config")
                    
            return config
        except Exception as e:
            logger.error(f"Error loading email configuration: {e}")
            raise
    
    def connect(self) -> bool:
        """Establish SMTP connection."""
        try:
            context = ssl.create_default_context()
            self.smtp_server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            self.smtp_server.starttls(context=context)
            self.smtp_server.login(self.config['email'], self.config['password'])
            logger.info("SMTP connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            return False
    
    def disconnect(self):
        """Close SMTP connection."""
        if self.smtp_server:
            self.smtp_server.quit()
            logger.info("SMTP connection closed")
    
    def send_job_application(self, 
                           recipient_email: str,
                           company_name: str,
                           position_title: str,
                           resume_path: Path,
                           cover_letter_path: Path,
                           custom_message: Optional[str] = None) -> bool:
        """
        Send job application email with resume and cover letter attachments.
        
        Args:
            recipient_email: Recipient's email address
            company_name: Name of the company
            position_title: Job position title
            resume_path: Path to generated resume PDF
            cover_letter_path: Path to generated cover letter PDF
            custom_message: Optional custom message to include
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.config['sender_name']} <{self.config['email']}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"Ansökan till {position_title} - {self.config['sender_name']}"
            
            # Create email body
            body = self._create_email_body(company_name, position_title, custom_message)
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Attach resume
            if resume_path.exists():
                with open(resume_path, 'rb') as file:
                    resume_attachment = MIMEApplication(file.read(), _subtype='pdf')
                    resume_attachment.add_header('Content-Disposition', 
                                               f'attachment; filename="CV_{self.config["sender_name"].replace(" ", "_")}.pdf"')
                    msg.attach(resume_attachment)
                logger.info(f"Resume attached: {resume_path}")
            
            # Attach cover letter
            if cover_letter_path.exists():
                with open(cover_letter_path, 'rb') as file:
                    cover_attachment = MIMEApplication(file.read(), _subtype='pdf')
                    cover_attachment.add_header('Content-Disposition', 
                                              f'attachment; filename="Personligt_brev_{self.config["sender_name"].replace(" ", "_")}.pdf"')
                    msg.attach(cover_attachment)
                logger.info(f"Cover letter attached: {cover_letter_path}")
            
            # Send email
            if not self.smtp_server:
                if not self.connect():
                    return False
            
            self.smtp_server.send_message(msg)
            logger.info(f"Job application sent successfully to {recipient_email} for {position_title} at {company_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send job application email: {e}")
            return False
    
    def _create_email_body(self, company_name: str, position_title: str, custom_message: Optional[str] = None) -> str:
        """Create professional email body for job application."""
        
        base_message = f"""Hej,

Jag skickar med denna ansökan till tjänsten som {position_title} på {company_name}.

Bifogat finner ni mitt CV och personliga brev som är anpassade för denna specifika tjänst. Mina kvalifikationer och erfarenheter matchar väl de krav som ställs för rollen.

Jag ser fram emot att höra från er och möjligheten att diskutera hur jag kan bidra till {company_name}.

Med vänliga hälsningar,
{self.config['sender_name']}
{self.config['email']}"""

        if custom_message:
            base_message += f"\n\nTillägg:\n{custom_message}"
        
        return base_message
    
    def send_bulk_applications(self, applications: List[Dict]) -> Dict[str, bool]:
        """
        Send multiple job applications.
        
        Args:
            applications: List of application dictionaries containing:
                - recipient_email
                - company_name  
                - position_title
                - resume_path
                - cover_letter_path
                - custom_message (optional)
                
        Returns:
            Dict mapping application ID to success status
        """
        results = {}
        
        if not self.connect():
            logger.error("Cannot establish SMTP connection for bulk sending")
            return results
        
        try:
            for i, app in enumerate(applications):
                app_id = f"{app['company_name']}_{app['position_title']}"
                logger.info(f"Sending application {i+1}/{len(applications)}: {app_id}")
                
                success = self.send_job_application(
                    recipient_email=app['recipient_email'],
                    company_name=app['company_name'],
                    position_title=app['position_title'],
                    resume_path=Path(app['resume_path']),
                    cover_letter_path=Path(app['cover_letter_path']),
                    custom_message=app.get('custom_message')
                )
                
                results[app_id] = success
                
                # Add delay between emails to avoid being flagged as spam
                import time
                time.sleep(2)
                
        finally:
            self.disconnect()
        
        return results


def create_email_template_config():
    """Create a template email configuration file."""
    template_config = {
        'smtp_server': 'smtp.gmail.com',  # För Gmail
        'smtp_port': 587,
        'email': 'din@email.com',
        'password': 'ditt-app-lösenord',  # Använd app-specifikt lösenord för Gmail
        'sender_name': 'Ditt Fullständiga Namn',
        'signature': 'Med vänliga hälsningar,\nDitt Namn\nTelefon: +46 70 123 45 67'
    }
    
    config_path = Path('data_folder/email_config.yaml')
    with open(config_path, 'w', encoding='utf-8') as file:
        yaml.dump(template_config, file, default_flow_style=False, allow_unicode=True)
    
    print(f"Email configuration template created at: {config_path}")
    print("Please edit this file with your actual email credentials.")
    return config_path


if __name__ == "__main__":
    # Create template configuration
    create_email_template_config()
