#import pypyodbc as pyodbc
import pyodbc
from Database import config
from lib.log import log


class MsSql:
    """
    This class does the MS SQL interaction 
    """

    def __init__(self):
        
        conn = pyodbc.connect(config.conn_str)
        
        #conn = pyodbc.connect('Driver={' + MS_SQL.DRIVER + '};'
         #                     'Server=' + MS_SQL.SERVER + ';'
          #                    'Database=' + MS_SQL.DATABASE + ';'
           #                   'UID=' + MS_SQL.UID + ';'
            #                  'PWD=' + MS_SQL.PASSWORD + ';')
        self.cursor = conn.cursor()

    def get_data(self):
        tables = {}
        for table in config.TABLES:
            data = self.get_table_data(table)
            tables[table] = data
        return tables

    def get_table_data(self, table):
        try:
            columns = self.cursor.columns(table=table.split(".")[-1])
            column_name = []
            for row in columns:
                column_name.append(row.column_name)
            query = "SELECT * FROM {};".format(table)
            rows = self.cursor.execute(query)
            data = []
            for row in rows:
                column_data = list(row)
                column_dict = dict(zip(column_name, column_data))
                data.append(column_dict)
            response = data
        except Exception as error:
            log.error("{} error: {}".format(table, error))
            response = str(error)
        finally:
            return response
