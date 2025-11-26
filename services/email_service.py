import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.smtp_config import SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT

class EmailService:

    @staticmethod
    async def send_email_smtp(to_email, subject, html_body):

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email

        msg.attach(MIMEText(html_body, "html"))

        try:
            server = aiosmtplib.SMTP(
                hostname=SMTP_SERVER,
                port=SMTP_PORT,
                start_tls=True
            )

            # 🔥 Aqui você usa await
            await server.connect()
            await server.starttls()
            await server.login(SMTP_USER, SMTP_PASSWORD)

            await server.sendmail(SMTP_USER, to_email, msg.as_string())

            await server.quit()

            return True
        
        except Exception as e:
            print("Erro ao enviar email:", e)
            return False

