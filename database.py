import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

database_driver = os.getenv('DATABASE_DRIVER')
database_username = os.getenv('DATABASE_USERNAME')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')
database_name = os.getenv('DATABASE_NAME')
database_url = os.getenv('DATABASE_URL')

print(database_url)

url = URL.create(
    drivername=database_driver,
    username=database_username,
    password=database_password,
    host=database_host,
    port=database_port,
    database=database_name    
)


print(url)

# DATABASE_URL = "postgresql+psycopg2://postgres:rootd@localhost:5432/lolas_db"

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()