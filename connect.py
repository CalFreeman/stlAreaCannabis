#!/usr/bin/python
import psycopg2
import json
import sys
from config import config
from psycopg2 import connect, Error

def dataFetch():
    # use Python's open() function to load the JSON data and return
    with open("./bin/final.json", "r") as json_file:
        record_list = json.load(json_file)
    return record_list

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

        #test json loader and parser
        dataFetched = dataFetch()
        #print(dataFetched)
        item_len = len(dataFetched)
        for num in range(0,item_len):
            print(dataFetched[num])

        # postgres_insert_query = """ INSERT INTO json_data (id, brand_col, gram_col, image_col, name_col, price_col, qty_col, status_col, strain_col, type_col) VALUES (%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"""
        # record_to_insert = ("5231b533-ba17-4787-98a3-f2df37de2ad7", "brandTest", 1, "testImg", "testName", 11, 12, "testStatus", "testStrain", "testType")
        # cur.execute(postgres_insert_query, record_to_insert)
        # conn.commit()
        # count = cur.rowcount
        # print(count, "Record inserted successfully")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        #print(db_version)

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