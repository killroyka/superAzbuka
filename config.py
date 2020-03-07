from decouple import config
from peewee import SqliteDatabase
from playhouse.db_url import connect

DB = connect(config("DATABASE_URL", default='sqlite:///bot.db'))
TOKEN = config('TOKEN')
PORT = config('PORT', default=8443)
HEROKU_APP_NAME = config('HEROKU_APP_NAME', default=None)
