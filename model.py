from peewee import *
from os import path

current_dir = path.dirname(__file__)
db_path = path.join(current_dir, 'log.db')
db = SqliteDatabase(db_path)

class Log(Model):
    line = CharField()
    api = CharField()
    endpoint = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db
