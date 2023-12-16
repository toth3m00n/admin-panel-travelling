import os
from app import create_app
from app.database import db
from dotenv import load_dotenv

load_dotenv()

app = create_app()
app.config.from_object(os.environ.get('APP_SETTINGS'))

if __name__ == '__main__':
    app.run()
