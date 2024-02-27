# from sqlalchemy.engine import URL
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy_utils import database_exists, create_database

import time
import psycopg2
from psycopg2 import OperationalError

from dotenv import load_dotenv
import os

load_dotenv()


DB_DRIVERNAME = os.getenv('POSTGRES_DRIVERNAME', default='postgresql')
DB_USERNAME = os.getenv('POSTGRES_USER', default='postgres')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', default='postgres')
DB_HOST = os.getenv('POSTGRES_HOST', default='localhost')
DB_PORT = os.getenv('POSTGRES_PORT', default='5432')
DB_DATABASE = os.getenv('POSTGRES_DB', default='postgres')

CELERY_USER = os.getenv('CELERY_USER')
CELERY_PASSWORD = os.getenv('CELERY_PASSWORD')
CELERY_HOST = os.getenv('CELERY_HOST')
CELERY_PORT = os.getenv('CELERY_PORT')


def create_conn():
    conn = None
    while not conn:
        try:
            conn = psycopg2.connect(
                dbname=DB_DATABASE,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
        except OperationalError as e:
            print(e)
            time.sleep(5)
    return conn


# def __get_db_url():
#     return URL.create(
#         drivername=DB_DRIVERNAME,
#         username=DB_USERNAME,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT,
#         database=DB_DATABASE
#     )


def make_celery():
    return Celery(
        'tasks',
        broker=f'amqp://{CELERY_USER}:{CELERY_PASSWORD}@{CELERY_HOST}:{CELERY_PORT}/',
        backend='rpc://'
    )


engine = create_engine(f'{DB_DRIVERNAME}://', creator=create_conn, echo=True)

session_db = sessionmaker(engine)

# if not database_exists(engine.url):
#     create_database(engine.url)
