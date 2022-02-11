from .table_relation import TableRelation
import mysql.connector
import yaml

# TODO: no Pk
DEFAULT_CONFIG = {
    'host': "localhost",
    'port': "3307",
    'user': "root",
    'password': "root",
    'database': "cs254"
}

PURPLE = '\033[35m'
GREEN = '\033[32m'
CLEAR = '\033[0m'

class HORMError(Exception):
    def __init__(self, value):
        self.value = value
 
    def __str__(self):
        return(repr(self.value))

class MYSQLConnection():
    def __init__(self, config_dict=None, yaml_file_path=None, log_sql=False):
        if yaml_file_path:
            try:
                with open(yaml_file_path, 'r') as yml:
                    con = yaml.safe_load(yml)
            except FileNotFoundError:
                con = DEFAULT_CONFIG
        elif config_dict:
            con = config_dict

        self.db = mysql.connector.connect(**con)
        self.cursor = self.db.cursor(dictionary = True)
        self.log_sql = log_sql

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params = params)

        if self.log_sql: self.log()

    def log(self):
        if self.cursor._executed:
            try:
                executed = self.cursor._executed.decode('utf-8')
            except AttributeError:
                executed = self.cursor._executed

        else:
            executed = '(Nothing executed yet)'
        print(f"{ PURPLE }SQL: { GREEN }{ executed } { CLEAR }")
            

class Table:
    """Base behaviour of a table"""

    connection = None 
    cursor = None 
    # PRIMARY_KEY is assumed to be autoincrementing
    PRIMARY_KEY = None
    relations = None

    table_name = None
    column_names = None

    log_sql = True

    def __init__(self, **args):
        """
        Gets column names from the table and makes them as instance variables
        """
        self.__in_db = False

        # set initial val as None
        for field in self.column_names:
            setattr(self, field, None)

        for key, val in args.items():
            # raise error if key is not present in column
            if key not in self.column_names: raise HORMError('%s is not a column in %s table' % (key, self.table_name))

            setattr(self, key, val)
        
        # set relations
        if self.relations is not None:
            for relation in self.relations:
                if isinstance(relation._class, str):
                    relation._class = Table.get_sub_class(relation._class)

                setattr(self, relation.name, TableRelation(relation=relation, base_record_obj=self, base_table_class=Table))

    def mark_as_created(self):
        self.__in_db = True
        return self

    def mark_as_deleted(self):
        self.__in_db = False
        return self

    def save(self):
        """Saves the chages to db"""

        # call self.update if __in_db
        if self.__in_db == True:
            return self

        # sql_query_temp => Eg- INSERT INTO students (id, name, gender, age) VALUES (%s, %s, %s, %s);
        insert_sql = "INSERT INTO {table_name} ({columns}) VALUES ({values});"
        values = [getattr(self, column) for column in self.column_names]
        
        # Eg- ["%s", "%s"]
        values_placehorder = ["%s"] * len(self.column_names)

        sql_query_temp = insert_sql.format(
                    table_name = self.table_name,
                    columns = ', '.join(self.column_names),
                    values = ', '.join(values_placehorder)
                    )

        self.execute_and_commit(sql_query_temp, values)

        # update the PRIMARY_KEY field value of the instance
        setattr(self, self.PRIMARY_KEY, self.cursor.lastrowid)

        # mark as present in db
        self.mark_as_created()
        return self

    def update(self, **args):
        if self.__in_db == False:
            raise HORMError("Record in not in table.")

        # update_query Eg- "name= %(name)s, age= %(age)s"
        update_query = ', '.join(
            [f"{field}= %({field})s" for field, val in args.items()])

        # Eg- UPDATE student SET name= %(name)s, age= %(age)s WHERE id = 1;
        sql_query = f"UPDATE { self.table_name } SET { update_query } WHERE { self.PRIMARY_KEY } = { self.primary_key_value() };"

        self.execute_and_commit(sql_query, args)

        for field, val in args.items():
            setattr(self, field, val)

        return self

    def destroy(self):
        delete_sql = f"DELETE FROM {self.table_name} WHERE {self.PRIMARY_KEY} = %s;"
        self.execute_and_commit(delete_sql, (self.primary_key_value(),))

        return self.mark_as_deleted()

    def primary_key_value(self):
        return getattr(self, self.PRIMARY_KEY)

    @classmethod
    def create(cls, **args):
        return cls(**args).save()

    @classmethod
    def all(cls, limit=1000):
        cls.execute(f"Select * from { cls.table_name } LIMIT { limit };")
        return cls.to_objects(
            cls.cursor.fetchall()
        )

    @classmethod
    def where(cls, **args):
        # where_query Eg- "id = %(id)s and name = %(name)s"
        where_query = ' and '.join(
            [f"{field}= %({field})s" for field, val in args.items()])

        # Eg- Select * from student where gender= %(gender)s and age= %(age)s ;
        sql_query = f"Select * from { cls.table_name } where { where_query } ;"

        cls.execute(sql_query, args)

        return cls.to_objects(
            cls.cursor.fetchall()
        )    

    @classmethod
    def find(cls, id):
        """Finds the record using `primary key` and returns it as a object
        
        returns None if record is not found
        """
        cls.execute(f"Select * from { cls.table_name } where { cls.PRIMARY_KEY }=%s LIMIT 1;", (id,))
        record = cls.cursor.fetchone()

        # return if not record found
        if record is None:
            return None

        arg = {}
        # make args
        for field, val in record.items():
            arg[field] = val

        # reset cursor
        cls.cursor.reset()

        return cls(**arg).mark_as_created()

    @classmethod
    def to_objects(cls, arr):
        """
        Converts a array of dicts(args) to array of Class instances.

        Records are assumed to be in db.
        """
        return [cls(**arg).mark_as_created() for arg in arr]

    @classmethod
    def describe_table(cls):
        """
        returns a dict of (`describe $table`)
        """
        cls.execute(f"describe { cls.table_name };")
        return cls.cursor.fetchall()

    @classmethod
    def tables(cls):
        cls.execute("show tables")
        for x in cls.cursor:
            print(x)

    @classmethod
    def execute(cls, sql, params=None):
        """Verifily deatails"""
        if cls.table_name is not None:
            cls.connection.execute(sql, params)
        else:
            raise HORMError('Table name cannot be None. (Try setting table_name)')

    @classmethod
    def execute_and_commit(cls, sql, params=None):
        cls.execute(sql, params)
        cls.connection.db.commit()

    @classmethod
    def connect(cls, config_dict=None, yaml_file_path=None):
        cls.connection = MYSQLConnection(config_dict, yaml_file_path, cls.log_sql)
        cls.cursor = cls.connection.cursor

    def __eq__(self, other):
        for field in self.column_names:
            if getattr(self, field) != getattr(other, field):
                return False

        return True

    def __str__(self):
        """<ClasName(col= val, .....)>"""
        col_val = [ f'{ key }= { self.__dict__[key] }' for key in self.__dict__ ]
        return '<%s(%s)>' % (type(self).__name__, ', '.join(col_val))

    def __init_subclass__(cls):
        if Table.connection is not None:
            cls.connection = Table.connection
            cls.cursor = Table.cursor
        else:
            cls.connect(config_dict=DEFAULT_CONFIG)

        desc_table = cls.describe_table()
        # set column_names
        cls.column_names = [row['Field'] for row in desc_table]

        # find PRIMARY KEY
        for field_ppt in desc_table:
            if field_ppt['Key'] == 'PRI':
                cls.PRIMARY_KEY = field_ppt['Field']
                break

    @classmethod
    def get_sub_class(cls, cls_str):
        for c in cls.__subclasses__():
            if c.__name__ == cls_str:
                return c
