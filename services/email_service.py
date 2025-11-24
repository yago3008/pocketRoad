import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.smtp_config import SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT

class EmailService:
    @staticmethod
    def send_email_smtp(to_email, subject, html_body):
        
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = SMTP_USER
            msg["To"] = to_email

            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, to_email, msg.as_string())

            return True

        except Exception as e:
            print("Erro ao enviar email:", e)
            return False
