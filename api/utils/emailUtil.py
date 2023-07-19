from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from starlette.config import Config
from typing import List

# Load .env

config = Config(".env")

print(config("MAIL_USERNAME"))

print("hello")

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM =  config("MAIL_FROM"),
    # MAIL_PORT =  config("MAIL_PORT"),
    # MAIL_SERVER =  config("MAIL_SERVER"),
    # MAIL_STARTTLS =  config("MAIL_STARTTLS"),
    # MAIL_SSL_TLS =  config("MAIL_SSL_TLS"),
    # USE_CREDENTIALS =  config("USE_CREDENTIALS"),
    # VALIDATE_CERTS =  config("VALIDATE_CERTS"),
)

print(conf)


async def send_email(subject: str,
                     recipient: List,
                     message : str
                     ):
    message = MessageSchema(
        subject=subject,
        recipients=recipient,
        body=message,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
    
    
    


