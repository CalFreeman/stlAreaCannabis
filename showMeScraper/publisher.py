#!/usr/bin/python
import psycopg2
import json
import sys
import urllib
import uuid
import subprocess
import urllib.request
import random
from config import config
from psycopg2 import connect, Error
def fetchJson(json_url):
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    return html

# fetch url to scrap
def fetchUrlpsqlQuery(columnName, table, dispensary_id):
    psql_select_Query = "select " + columnName + " from " + table + " where id = '" + dispensary_id + "';"
    return psql_select_Query

# not working
def publishUrlJson(json_blob):
    uuid = random.randint(0, 10000)
    psql_publish_Query = """ INSERT INTO json_blob (id, info) VALUES (%s, %s) """
    record_to_insert = (uuid, json_blob)
    print(uuid)
    return psql_publish_Query, record_to_insert

def connect():
    columnName = "flower_url"
    table = "dispensaries"
    dispensary_id = "947808ec-f091-4507-bdc5-a1fb065f689d" 
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        #print ("\ncreated cursor object:", cur)

        #fetch url end point to grab json_blob
        url = fetchUrlpsqlQuery(columnName, table, dispensary_id)
        #print ("fetching: " + url)
        cur.execute(url)
        json_url = cur.fetchone()

        json_blob = fetchJson(json_url[0])

        publisher_data = publishUrlJson(json_blob)

        print(publisher_data[0]) # [0] == uuid
        query_to_run = publisher_data[0]
        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        byteToString = publisher_data[1][1].decode('utf8').replace("'", '"') # [1] == json_blob
        generatedId = str(publisher_data[1][0])
        print(generatedId)
        record_to_insert = (generatedId, json.dumps(byteToString))

        cur.execute(query_to_run, record_to_insert)

        print("brkpt")

        conn.commit()
        
        print("test")
        count = cur.rowcount
        print(count, "Record inserted successfully")

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