from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import sys
from dotenv import load_dotenv
import os

dotenv_path = "./.env"
load_dotenv(dotenv_path)
try:
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost/ascend")
    print("Connected to the database")
except SQLAlchemyError as e:
    print(f"Error: {e}")
    sys.exit(1)
