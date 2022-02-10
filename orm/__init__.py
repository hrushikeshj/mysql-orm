"""
Author: Hrushikesh J
An ORM for MySql

See https://github.com/hrushikeshj/mysql-orm for more information.
"""
from .table import Table
from .table_relation import has_many, belongs_to, TableRelation

def get_table(table_name):
   return  type(
        table_name,
        (Table,),
        {
           "table_name": table_name
        }
    )
