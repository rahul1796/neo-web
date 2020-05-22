#import pypyodbc as pyodbc
from flask import request
import pyodbc
from Database import config
from Database import constants as CONST
import pandas as pd
#from lib.log import log


class MsSql:
    """
    This class does the MS SQL interaction 
    """

    def __init__(self):
        
        self.conn = pyodbc.connect(config.conn_str)
        
        #conn = pyodbc.connect('Driver={' + MS_SQL.DRIVER + '};'
         #                     'Server=' + MS_SQL.SERVER + ';'
          #                    'Database=' + MS_SQL.DATABASE + ';'
           #                   'UID=' + MS_SQL.UID + ';'
            #                  'PWD=' + MS_SQL.PASSWORD + ';')
        self.cursor = self.conn.cursor()

    def get_data(self, param):
        tables_data = {}
        startDate = None
        endDate = None
        if param == CONST.CANDIDATES:
            startDate = request.args.get('start_date', '', type=str)
            endDate = request.args.get('end_date', '', type=str)
            tables = config.SQL_CANDIDATES_TABLE
        elif param == CONST.CANDIDATE_REG_ENROLL_DETAILS:
            tables = config.CANDIDATE_REG_ENROLL_DETAILS_TABLE
        elif param == CONST.CANDIDATE_REG_ENROLL_NON_MANDATORY_DETAILS:
            tables = config.CANDIDATE_REG_ENROLL_NON_MANDATORY_DETAILS_TABLE
        elif param == CONST.CANDIDATE_INTERVENTIONS:
            tables = config.CANDIDATE_INTERVENTIONS_TABLE
        elif param == CONST.CANDIDATE_INTERVENTION_TRACKER:
            tables = config.CANDIDATE_INTERVENTION_TRACKER_TABLE
        elif param == CONST.MAP_CANDIDATE_INTERVENTION_SKILLING:
            tables = config.MAP_CANDIDATE_INTERVENTION_SKILLING_TABLE
        else:
            tables = config.SQL_GENERAL_TABLES
        for table in tables:
            data = self.get_table_data(table, startDate, endDate)
            tables_data[table] = data
        return tables_data

    def get_table_data(self, table, startDate, endDate):
        try:
            data = []
            column_name = []
            columns = self.cursor.columns(table=table.split(".")[-1])
            for row in columns:
                column_name.append(row.column_name)
            if table == config.SQL_CANDIDATES_TABLE[0] and startDate and endDate:
                query = "SELECT * FROM {} WHERE modified_on BETWEEN '{}' AND '{}';".format(table, startDate, endDate)
            else:
                query = "SELECT * FROM {};".format(table)
            
            for df in pd.read_sql(query, self.conn, chunksize=100 ** 4):
                if 'EndTime' in df.columns:
                    df = df.drop('StartTime', 1)
                    df = df.drop('EndTime', 1)
                    df = df.fillna("null")
                    if table in config.REPLACE_EMPTY_STRING_TABLES:
                        df = df.replace("", "null")
                    
                dict_data = df.reset_index().to_dict(orient='records')
                data.append(dict_data)
            if not len(data):
                column_dict = {column_name[i]: "" for i in range(0, len(column_name))}
                column_dict.pop('StartTime', None)
                column_dict.pop('EndTime', None)
                data.append(column_dict)
            response = data
        except Exception as error:
            #log.error("{} error: {}".format(table, error))
            response = str(error)
        finally:
            return response