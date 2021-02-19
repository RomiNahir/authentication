import configparser
from sqlalchemy import create_engine
import warnings
import sqlite3




config = configparser.ConfigParser()

warnings.filterwarnings("ignore")
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')