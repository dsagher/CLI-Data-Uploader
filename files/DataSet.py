class DataSet:

    def __init__(self):
        self.column_lst = []
        self.unique_lst = []

    def add_columns(self, columns):
        self.column_lst.append(columns)
        
    def add_unique_values(self, unique_values):
        self.unique_lst.append(unique_values)
    
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
    
 
    def dicts(self):
        return self.dicts
    

    


dataset = DataSet()
    

