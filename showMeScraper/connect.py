#!/usr/bin/python
import psycopg2
import json
import sys
from config import config
from psycopg2 import connect, Error
import uuid

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

        # test json loader and parser
        dataFetched = dataFetch()
        item_len = len(dataFetched)

        #fetch companyId
        companyId = 
        for num in range(0,item_len):
            # generate UUID
            myuuid = uuid.uuid4()
            myuuidStr = str(myuuid)
            # insert data
            postgres_insert_query = """ INSERT INTO json_data (id, companies, brand, gram, image, name, price, qty, status, strain, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (myuuidStr, companyId, dataFetched[num]["brand_col"], dataFetched[num]["gram_col"], dataFetched[num]["image_col"], dataFetched[num]["name_col"], dataFetched[num]["price_col"], dataFetched[num]["qty_col"], dataFetched[num]["status_col"], dataFetched[num]["strain_col"], dataFetched[num]["type_col"])
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            print(count, "Record inserted successfully")

        # display the PostgreSQL database server version
        cur.execute('SELECT version()')
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