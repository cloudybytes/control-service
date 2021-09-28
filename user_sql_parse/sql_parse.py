import json

class Parse:

    def __init__(self, query, schema):
        self.from_table = ''
        self.join = []
        self.where = []
        self.select_columns = []
        self.group_by_column = []
        self.having_condition = []
        self.parsedQuery = {}
        self.query = query
        self.schema = schema
        self.aggr_function = ''
    
    def get_tokenized_elements(self):
        query = self.query
        query = query.lower()
        query = query.strip()
        tokenized_query = query.split()
        return tokenized_query
        
    
    def parse_query_string(self):
        tokenized_query = self.get_tokenized_elements()
        self.from_table = tokenized_query[tokenized_query.index('from')+1]
        self.parsedQuery['from_table'] = self.from_table
        self.select_columns = [x.strip(',') for x in tokenized_query[1:tokenized_query.index('from')] ]
        if self.select_columns[0] == "*":
            self.select_columns = list(self.schema[self.from_table])
        self.parsedQuery['select_columns'] = self.select_columns
        # join_type = tokenized_query[tokenized_query.index('join')-1]
        if 'join' in tokenized_query:
            join_type = "_".join(tokenized_query[tokenized_query.index(self.from_table)+1:tokenized_query.index('join')])
            join_to_table = tokenized_query[tokenized_query.index('join')+1]
            self.join.append(join_type)
            if tokenized_query[tokenized_query.index('join')+2] == 'on':
                join_column_1 = tokenized_query[tokenized_query.index('join')+3]
                join_column_2 = tokenized_query[tokenized_query.index('join')+5]
                self.join.extend(join_column_1.split('.'))            
                self.join.extend(join_column_2.split('.'))
            self.parsedQuery['join'] = self.join
        elif 'group' in tokenized_query:
            self.group_by_column = tokenized_query[tokenized_query.index('group')+2]
            having_function , having_operator, having_value = tokenized_query[tokenized_query.index('having')+1:]
            aggr_function , having_column = having_function.split('(')
            having_column=having_column.strip(")")
            having_value=having_value.strip("; ")
            self.aggr_function = aggr_function
            self.having_condition = [having_column,having_operator,having_value]
            self.parsedQuery['group_by_column'] = self.group_by_column
            self.parsedQuery['having_condition'] = self.having_condition
            self.parsedQuery['aggr_function'] = self.aggr_function

    def get_parsed_query(self):
        self.parse_query_string()
        return self.parsedQuery
