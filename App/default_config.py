import os
from dotenv import load_dotenv

load_dotenv()

#SQLALCHEMY_DATABASE_URI="sqlite:///temp-database.db"
SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY=os.getenv('SECRET_KEY')