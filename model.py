from peewee import *

db = SqliteDatabase('log.db')

class Log(Model):
    line = CharField()
    api = CharField()
    endpoint = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db
