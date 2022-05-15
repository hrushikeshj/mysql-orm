# MySql ORM

A simple Object Relational Mapper for MySql. Works with existing tables and the schema of the tables are automatically inferred.
### Install
```bash
pip install orm-mysql
```

## Connect to MySql
```python
from orm import Table

Table.connect(config_dict={
    'host': '<host_here>',
    'port': 3306,
    'user': '<user>',
    'password': '<password>',
    'database': '<database>'
})
```

## Create a class for a table
Create a class that inherits from `Table`. Initialize the class variable `table_name` with the name of the table, here 'student'
```python
from orm import Table
Table.connect(config_dict=CONFIG)

class Student(Table):
    table_name = 'student'
```

#### OR use `get_table()`
```python
from orm import Table, get_table
Table.connect(config_dict=CONFIG)

Student = get_table('student')
```

# Insert data
### Using `save()`
```python
new_student = Student(name='hrushi', age=19, gender='M')
new_student.age = 20
new_student.save()
```

### Using `create()`
```python
new_student = Student.create(name='hrushi', age=19, gender='M')
```

# Query data
### Using `where()`
```python
students = Student.where(age=19, gender='F')

for stu in students:
    print(stu.name)
```

### Using `find()`
Find a single record based on PRIMARY KEY.
```python
# find student where id(PK) = 2
student = Student.find(2)

print(student.name)
```

## Delete a record
```python
student = Student.find(2)
student.destroy()
```

## Relations
`has_many` and `belongs_to` can be used to show relationships between tables.
```python
from orm import Table, has_many, belongs_to

class Article(Table):
    table_name = 'articles'

    relations = [
        belongs_to(name='author', _class='Author', foreign_key='author_id', primary_key='id')
    ]

class Author(Table):
    table_name = 'authors'
    
    relations = [
        has_many(name='articles', _class='Article', foreign_key='author_id')
    ]

```

#### Get all the books written a Author
```python
auth = Author.find(2)
articles = auth.articles()
for art in articles:
    print(art.title)
```

#### Get Author of a book
```python
art = Article.find(5)
author = art.author()
print(author.name)
```
