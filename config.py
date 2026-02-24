import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY =  '2485fdb6dad2ad10d3e8ae066b635f9ca94fbd2815e275eda1c2358364530d59'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

    # Email settings (used for sending results)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT =  587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('rishithamb5@gmail.com')
    MAIL_PASSWORD = os.environ.get('Rishi@702213')
    MAIL_DEFAULT_SENDER = 'noreply@smarthire.ai'