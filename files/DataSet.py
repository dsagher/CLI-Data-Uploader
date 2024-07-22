class DataSet:

    def __init__(self):
        self.column_lst = []
        self.unique_lst = []

    def add_columns(self, columns):
        self.column_lst.append(columns)
        
    
    def add_unique_values(self, key, unique_values):
        self.unique_lst.append((key, unique_values))
    
    def add_dict(self, lst_of_dcts):
        self.dict_lst.append(lst_of_dcts)
    
    def row_count():
        pass
    
    def column_count():
        pass

    def shape():
        pass

    @property   
    def columns(self):
        return self.column_lst
    
    @property
    def values(self):
        return self.unique_lst
    

