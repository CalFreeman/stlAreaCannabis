#!/usr/bin/python
import psycopg2
import json
import sys
from config import config
from psycopg2 import connect, Error

def test():
    print('test')

def connect():

    # accept command line arguments for the Postgres table name
    if len(sys.argv) > 1:
        table_name = '_'.join(sys.argv[1:])
    else:
        # ..otherwise revert to a default table name
        table_name = "json_data"

    print ("\ntable name for JSON data:", table_name)

    # use Python's open() function to load the JSON data
    with open("./bin/final.json") as json_data:

        # use load() rather than loads() for JSON files
        record_list = json.load(json_data)

        if type(record_list) == list:
            first_record = record_list[0]
            # get the column names from the first record
            columns = list(first_record.keys())
            print ("\ncolumn names:", columns)
            table_name = "json_data"
            sql_string = 'INSERT INTO {} '.format( table_name )
            sql_string += "(" + ', '.join(columns) + ")\nVALUES "
            # enumerate over the record
            for i, record_dict in enumerate(record_list):

                # iterate over the values of each record dict object
                values = []
                for col_names, val in record_dict.items():

                    # Postgres strings must be enclosed with single quotes
                    if type(val) == str:
                        # escape apostrophies with two single quotations
                        val = val.replace("'", "''")
                        val = "'" + val + "'"

                    values += [ str(val) ]


    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        test()
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()