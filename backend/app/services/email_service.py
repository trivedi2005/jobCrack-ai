import logging
import smtplib
from email.message import EmailMessage
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_password_reset_email(email: str, reset_url: str) -> None:
    if not all((settings.SMTP_HOST, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM_EMAIL)):
        if settings.ENVIRONMENT == "production":
            raise RuntimeError("SMTP is not configured")
        logger.warning("SMTP is not configured. Development password reset URL for %s: %s", email, reset_url)
        return

    message = EmailMessage()
    message["Subject"] = "Reset your JobCrack AI password"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = email
    message.set_content(
        f"Use this link to reset your password. It expires in {settings.PASSWORD_RESET_EXPIRE_MINUTES} minutes:\n\n{reset_url}\n\n"
        "If you did not request this, you can ignore this email."
    )
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
        if settings.SMTP_USE_TLS:
            server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(message)