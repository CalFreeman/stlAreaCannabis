#!/usr/bin/python
import psycopg2
import json
import sys
from config import config
from psycopg2 import connect, Error

def test():
    # brand_col = []
    # gram_col = []
    # image_col = []
    # name_col = []
    # price_col = []
    # qty_col = []
    # status_col = []
    # strain_col = []
    # type_col = []

    print('test')
    # accept command line arguments for the Postgres table name
    if len(sys.argv) > 1:
        table_name = '_'.join(sys.argv[1:])
    else:
        # ..otherwise revert to a default table name
        table_name = "json_data"

    print ("\ntable name for JSON data:", table_name)

    # use Python's open() function to load the JSON data
    with open("./bin/final.json", "r") as json_file:

        record_list = json.load(json_file)
        print ("\nJSON records object type:", type(record_list)) # should return "<class 'list'>"
        item_len = len(record_list)
        #print(item_len)
        for num in range(0,item_len):
            print(record_list[num])
            print(num)
        
        # brand_col.append(record_list[num]["brand_col"])
        # gram_col.append()
        # image_col.append()
        # name_col.append()
        # price_col.append()
        # qty_col.append()
        # status_col.append()
        # strain_col.append()
        # type_col.append()

        # for item in record_list("json_data"):
        #     print(record_list[int(item)])
        # # concatenate the SQL string
        # table_name = "json_data"
        # sql_string = "INSERT INTO %s (%s)\nVALUES %s" % (
        #     table_name,
        #     ', '.join(columns),
        #     values_str
        # )

def connect():
    try:
    # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        print ("\ncreated cursor object:", cur)

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        #test json loader and parser
        test()
        #test post
        postgres_insert_query = """ INSERT INTO json_data (id, brand_col, gram_col, image_col, name_col, price_col, qty_col, status_col, strain_col, type_col) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"""
        record_to_insert = ("5231b533-ba17-4787-98a3-f2df37de2ad7", "brandTest", 1, "testImg", "testName", 11, 12, "testStatus", "testStrain", "testType")
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully")

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