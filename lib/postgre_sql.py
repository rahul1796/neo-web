import psycopg2
import pandas as pd
from Database import config
#import config.postgre_sql_config as POSTRESQL
#from lib.log import log


class PostgreSql:
    """
    This class does the MS SQL interaction
    """

    def __init__(self):
        self.conn = psycopg2.connect(
            host=config.postgre_SERVER,
            database=config.postgre_DATABASE,
            user=config.postgre_USER,
            password=config.postgre_PASSWORD
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def get_data(self):
        tables = {}
        for table in POSTRESQL.TABLES:
            data = self.get_table_data(table)
            tables[table] = data
        return tables

    def get_table_data(self, table):
        try:
            data = []
            query = "SELECT * FROM {} LIMIT 50;".format(table)
            for df in pd.read_sql(query, self.conn, chunksize=400 ** 4):
                df = df.fillna('Na')
                dict_data = df.reset_index().to_dict(orient='records')
                data.append(dict_data)
            response = data
        except Exception as error:
            #log.error("{} error: {}".format(table, error))
            response = str(error)
        finally:
            return response

    def __del__(self):
        self.cursor.close()
        self.conn.close()
