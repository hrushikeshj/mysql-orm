import pytest
from orm import Table, has_many, belongs_to

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
print(Author.find(1).art.where(id=2))
print(Article.find(3).art())
#Article.create(title="t3", content="c3", author_id='1')

"""
Table student with following schema is alredy created in db

+--------+-------------+------+-----+---------+----------------+
| Field  | Type        | Null | Key | Default | Extra          |
+--------+-------------+------+-----+---------+----------------+
| id     | int(10)     | NO   | PRI | NULL    | auto_increment |
| name   | varchar(15) | NO   |     | NULL    |                |
| gender | char(1)     | YES  |     | NULL    |                |
| age    | int(3)      | YES  |     | NULL    |                |
+--------+-------------+------+-----+---------+----------------+
"""

class Student(Table):
    table_name = 'student'

def test_connection():
    assert Student.cursor is not None, "connection should me made"

def test_schema():
    assert Student.column_names() == ['id', 'name', 'gender', 'age']

def test__init__():
    """
    Test attributes are initialized properly
    """
    new_stu = Student(name='test-name', age=20, gender='F')
    assert new_stu.name == 'test-name'
    assert new_stu.age == 20
    assert new_stu.gender == 'F'

def test_save():
    new_stu = Student(name='test-name', age=21, gender='F')
    new_stu.save()
    assert new_stu.primary_key_value() is not None

def test_create():
    new_stu = Student.create(name='test-name', age=22, gender='M')
    assert isinstance(new_stu, Student)
    assert new_stu.primary_key_value() is not None

def test_find():
    new_stu = Student.create(name='test-name', age=22, gender='M')
    pk_value = new_stu.primary_key_value()
    assert Student.find(pk_value) == new_stu

def test_destroy():
    new_stu = Student.create(name='test-name', age=23, gender='f')
    pk_value = new_stu.primary_key_value()

    new_stu.destroy()

    # assert record is deleted
    assert Student.find(pk_value) is None
