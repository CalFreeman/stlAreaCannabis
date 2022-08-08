#!/usr/bin/python
import psycopg2
import json
import sys
import urllib
import uuid
import subprocess
from config import config
from psycopg2 import connect, Error

# fetch url to scrap
def fetchUrlpsqlQuery(columnName, table, dispensary_id):
    psql_select_Query = "select " + columnName + " from " + table + " where id = '" + dispensary_id + "';"
    return psql_select_Query

def publish():
    subprocess.run(["../bin/data_parser.sh", "947808ec-f091-4507-bdc5-a1fb065f689d"])

def dataFetch():
    # use Python's open() function to load the JSON data and return
    with open("../bin/final.json", "r") as json_file:
        record_list = json.load(json_file)
    return record_list

def connect():
    columnName = "flower_url"
    table = "dispensaries"
    dispensary_id = "947808ec-f091-4507-bdc5-a1fb065f689d" 
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        print ("\ncreated cursor object:", cur)

        #need to provid param values
        url = fetchUrlpsqlQuery(columnName, table, dispensary_id)
        print (url)
        cur.execute(url)
        json_blob = cur.fetchone()
        print(json_blob)
        #publish()

        # # test json loader and parser
        # dataFetched = dataFetch()
        # item_len = len(dataFetched)

        # #fetch dispensary_id
        # dispensary_id = '947808ec-f091-4507-bdc5-a1fb065f689d'
        # for num in range(0,item_len):
        #     # generate UUID
        #     myuuid = uuid.uuid4()
        #     myuuidStr = str(myuuid)
        #     # insert data
        #     postgres_insert_query = """ INSERT INTO json_data (id, companies, brand, gram, image, name, price, quantity, status, strain, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        #     record_to_insert = (myuuidStr, dispensary_id, dataFetched[num]["brand"], dataFetched[num]["gram"], dataFetched[num]["image"], dataFetched[num]["name"], dataFetched[num]["price"], dataFetched[num]["quantity"], dataFetched[num]["status"], dataFetched[num]["strain"], dataFetched[num]["type"])
        #     cur.execute(postgres_insert_query, record_to_insert)
        #     conn.commit()
        #     count = cur.rowcount
        #     print(count, "Record inserted successfully")

        # # display the PostgreSQL database server version
        # cur.execute('SELECT version()')
        # db_version = cur.fetchone()
        # print(db_version)

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