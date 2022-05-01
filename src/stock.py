class Stock():
    '''
    This class is an object representing a company and its share values
    Attributes:
        name - name of company
        value - worth of individual stocks
    '''

    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name + ": " + str(self.value)
