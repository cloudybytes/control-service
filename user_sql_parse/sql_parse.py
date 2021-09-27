import json

class Parse:

    def __init__(self, query, schema):
        self.from_table = []
        self.join = []
        self.where = []
        self.select_columns = []
        self.group_by_column = []
        self.having_condition = []
        self.parsedQuery = {}
        self.query = query
        self.schema = schema
    
    def get_tokenized_elements(self):
        query = self.query
        query = query.lower()
        query = query.strip()
        tokenized_query = query.split()
        return tokenized_query
        
    
    def parse_query_string(self):
        tokenized_query = self.get_tokenized_elements()
        self.from_table = [tokenized_query[tokenized_query.index('from')+1]]
        self.parsedQuery['from_table'] = self.from_table
        self.select_columns = [x.strip(',') for x in tokenized_query[1:tokenized_query.index('from')] ]
        self.parsedQuery['select_columns'] = self.select_columns
        # join_type = tokenized_query[tokenized_query.index('join')-1]
        join_type = " ".join(tokenized_query[tokenized_query.index(self.from_table[0]):tokenized_query.index('join')])
        join_to_table = tokenized_query[tokenized_query.index('join')+1]
        self.join.append(join_type)
        if tokenized_query[tokenized_query.index('join')+2] == 'on':
            join_column_1 = tokenized_query[tokenized_query.index('join')+3]
            join_column_2 = tokenized_query[tokenized_query.index('join')+5]
            self.join.extend(join_column_1.split('.'))
            self.join.extend(join_column_2.split('.'))




    def get_parsed_query(self):
        self.parse_query_string()
        return self.parsedQuery
