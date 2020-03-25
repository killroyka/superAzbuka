import peewee
import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class User(BaseModel):
    tg_id = peewee.BigIntegerField(index=True)
    full_name = peewee.CharField(index=True)

class Message(BaseModel):
    message_id = peewee.BigIntegerField()
    chat_id = peewee.BigIntegerField()
    text = peewee.TextField()
    tg_id = peewee.BigIntegerField()

