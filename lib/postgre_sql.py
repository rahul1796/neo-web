from flask import request
import psycopg2
import pandas as pd
from Database import config
from Database import constants as CONST
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

    def get_data(self, param):
        tables_data = {}
        startDate = None
        endDate = None
        if param == CONST.CANDIDATES:
            startDate = request.args.get('start_date', '', type=str)
            endDate = request.args.get('end_date', '', type=str)
            tables = config.CANDIDATES_TABLE
        elif param == CONST.NEO_BATCHES:
            tables = config.NEO_BATCHES_TABLE
        else:
            tables = config.GENERAL_TABLES
        for table in tables:
            data = self.get_table_data(table, startDate, endDate)
            tables_data[table] = data
        return tables_data

    def get_table_data(self, table, startDate, endDate):
        try:
            data = []
            if table == config.CANDIDATES_TABLE[0] and startDate and endDate:
                query = "SELECT * FROM {} WHERE modified_at BETWEEN '{}' AND '{}';".format(table, startDate, endDate)
            else:
                query = "SELECT * FROM {};".format(table)
            for df in pd.read_sql(query, self.conn, chunksize=100 ** 2):
                df = df.fillna('null')
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
