class DataSet:

    column_lst = list()
    unique_lst = list()

    def add_columns(self, columns):
        self.column_lst.append(columns)
        self._columns = self.column_lst
    
    def add_unique_values(self, unique_values):
        self.unique_lst.append(unique_values)
        self._values = self.unique_lst
    
    def row_count():
        pass
    
    def column_count():
        pass

    def shape():
        pass

    @property   
    def columns(self):
        return self._columns
    
    @property
    def values(self):
        return self._values