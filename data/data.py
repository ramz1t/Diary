from datetime import date, timedelta

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker
import string
from dotenv import load_dotenv
import os

load_dotenv()

'''symbols for key generation'''
symbols = string.digits + string.ascii_letters

Base = declarative_base()

Engine = create_engine('sqlite:///data/data.db')
Base.metadata.create_all(Engine)
Sessions = sessionmaker(bind=Engine)
SERVER_DOMAIN = 'http://127.0.0.1:8001'

'''dates of year start and end'''
TODAY = date.today()

YEAR_START = date(year=TODAY.year, month=9, day=1)
YEAR_END = date(year=TODAY.year, month=5, day=31) + timedelta(days=365)


DB_NAME = os.getenv('DB')
USERNAME = os.getenv('USERNAME')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
