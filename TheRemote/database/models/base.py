from peewee import *

class MetaData(Model):
    pass

class BaseAsset(Model):
    file_path = CharField()
    checksum = CharField()
    metadata = ForeignKeyField(MetaData)


