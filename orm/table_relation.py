class has_many:
    def __init__(self, name, _class, primary_key=None, foreign_key=None):
        self.name = name
        self._class = _class
        self.primary_key = primary_key
        self.foreign_key = foreign_key

class belongs_to:
    def __init__(self, name, _class, primary_key=None, foreign_key=None):
        self.name = name
        self._class = _class
        self.primary_key = primary_key
        self.foreign_key = foreign_key

def only_for_has_many(func):
    def wrapper(self, *args, **kwrgs):
        if isinstance(self.relation, has_many):
            return func(self, *args, **kwrgs)
        else:
            print("Only for has_many!!")

    return wrapper

class TableRelation:
    def __init__(self, base_table_class, relation, base_record_obj):
        self.base_table_class = base_table_class
        self.relation = relation
        self.pk = relation.primary_key
        self.fk = relation.foreign_key
        self.table = relation._class
        self.base_record_obj = base_record_obj
    
    @only_for_has_many
    def all(self):
        """Applies relation.
        
        Only for has_many"""

        return self.table.where(**{self.fk: self.base_record_obj.primary_key_value()})
    
    @only_for_has_many
    def where(self,  **args):
        args[self.fk] = self.base_record_obj.primary_key_value()

        return self.table.where(**args)
    
    def create(self, **args):
        """
        Sets the FK to the current objs PK value and creats a record
        """
        if isinstance(self.relation, has_many):
            args[self.fk] = self.base_record_obj.primary_key_value()
            return self.table.create(**args)

        else:
            print("Only for has_many")


    def __call__(self):
        if isinstance(self.relation, has_many):
            return self.all()
        
        elif isinstance(self.relation, belongs_to):
            """
            Eg- Articles and Authors
            Articles belings_to Authors

            SELECT * FORM authors WHERE id= fk_value

            `id` is the primary key of the table to which "articles" belong
            """
            rec = self.table.where(**{self.pk: getattr(self.base_record_obj, self.fk)})

            return rec[0] if rec else None
