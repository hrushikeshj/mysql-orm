import pytest
import os
from orm import Table, has_many, belongs_to

CONFIG = {
    'host': os.environ.get('ORM_MYSQL_HOST') or 'localhost',
    'port': os.environ.get('ORM_MYSQL_PORT') or 3306,
    'user': os.environ.get('ORM_MYSQL_USER'),
    'password': os.environ.get('ORM_MYSQL_PASSWORD'),
    'database': os.environ.get('ORM_MYSQL_DATABASE')
}

Table.connect(config_dict=CONFIG)

class Article(Table):
    table_name = 'articles'

    relations = [
        belongs_to(name='art', _class='Author', foreign_key='author_id', primary_key='id')
    ]

class Author(Table):
    table_name = 'authors'
    
    relations = [
        has_many(name='art', _class='Article', foreign_key='author_id')
    ]

#print(Table.get_sub_class('Article'))
#print(Author.find(1).art.where(id=2))
#print(Article.find(3).art())
#Article.create(title="t3", content="c3", author_id='1')

def test_connection():
    assert Author.cursor is not None, "connection should me made"

def test_h():
    assert 1==1
