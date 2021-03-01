import configparser
import mysql.connector #pip3 install mysql-connector-python

config = configparser.ConfigParser()
config.read('config.ini')


def connect():
    return mysql.connector.connect(host=config['database']['host'], 
    port=config['database']['port'],
    user=config['database']['user'],
    passwd=config['database']['passwd'],
    db=config['database']['db'])