import configparser

from mongoengine import Document, CASCADE, connect
from mongoengine.fields import StringField, ListField, ReferenceField

config = configparser.ConfigParser()
config.read('config.ini')
mongo_user = config.get('DB', 'USER_MONGO')
mongodb_pass = config.get('DB', 'PASS_MONGO')
db_name = config.get('DB', 'DB_NAME_MONGO')

connect(
    host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@pasichniuk.qpmb3z9.mongodb.net/{db_name}?retryWrites=true&w=majority",
    ssl=True)


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()


from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.schema import ForeignKey

import configparser
import pathlib

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

file_ini = pathlib.Path(__file__).joinpath('config.ini')
config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')

url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'

engine = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class author(Base):
    __tablename__ = "app_quotes_author"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(255))
    born_date = Column(String(255))
    born_location = Column(String(255))
    description = Column(String(255))


class quote(Base):
    __tablename__ = "app_quotes_quote"
    id = Column(Integer, primary_key=True)
    quote = Column(String(1500))
    author_id = Column(Integer, ForeignKey("app_quotes_author.id"))



class tag(Base):
    __tablename__ = "app_quotes_tag"
    id = Column(Integer, primary_key=True)
    tag = Column(String(255))


class tags_rel(Base):
    __tablename__ = "app_quotes_quote_tags"
    id = Column(Integer, primary_key=True)
    quote_id = Column(Integer, ForeignKey("app_quotes_quote.id"))
    tag_id = Column(Integer, ForeignKey("app_quotes_tag.id"))


for item in Author.objects.all():


    new_author = author(fullname=item.fullname,
                        born_date=item.born_date,
                        born_location=item.born_location,
                        description=item.description)


    session.add(new_author)

session.commit()

tags = []
for item in Quote.objects.all():
    tags += item.tags

tags = set(tags)

for i in tags:
    new_tag = tag(tag=i)

    session.add(new_tag)

session.commit()

all_authors = dict(session.query(author.fullname, author.id).all())
print(all_authors)

all_tags = dict(session.query(tag.tag, tag.id).all())
print(all_tags)


for item in Quote.objects.all():
    new_qute = quote(quote=item.quote, author_id=all_authors[item.author.fullname])
    session.add(new_qute)
    session.commit()

    for t in item.tags:

        new_tags_rel = tags_rel(quote_id=new_qute.id, tag_id=all_tags[t])

        session.add(new_tags_rel)

    session.commit()


