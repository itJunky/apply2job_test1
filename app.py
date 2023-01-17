from sqlalchemy import create_engine, select
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from random import randrange
import socket
import time

DB_USER = os.getenv('TEST_DB_USER')
DB_PASS = os.getenv('TEST_DB_PASS')
DB_HOST = os.getenv('TEST_DB_HOST')
DB_NAME = os.getenv('TEST_DB_NAME')

if DB_USER:
    print(f'Have credentials for DB_USER: {DB_USER}')
else:
    print('Use default credentials for DB')
    DB_USER = 'root'
    DB_PASS = 'change-me'
    DB_HOST = 'localhost'
    DB_NAME = 'webinar_test'

Base = declarative_base()
db_path = 'mysql+pymysql://' + DB_USER + ':' + DB_PASS + '@' + DB_HOST + '/' + DB_NAME
engine = create_engine(db_path, echo=False)
session = scoped_session(sessionmaker(bind=engine))


class First(Base):
    __tablename__ = 'first'
    id = Column(Integer, nullable=False, primary_key=True)
    firstname = Column(String(255))


class Last(Base):
    __tablename__ = 'last'
    id = Column(Integer, nullable=False, primary_key=True)
    lastname = Column(String(255))

def check():
    rnd = randrange(10) 
    slct = select(First.id, First.firstname, Last.lastname).select_from(First).join(Last, First.id == Last.id).filter_by(id=rnd)
    result = session.execute(slct).first()
    
    host = socket.gethostname()
    try:
        print(f'{result[0]} - {result[1]} {result[2]} AT {host}')
    except Exception as e:
        print(f'SOME ERROR: {e}')

while True:
    check()
    time.sleep(1)

