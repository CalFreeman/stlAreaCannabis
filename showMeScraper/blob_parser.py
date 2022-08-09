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

#TODO dynamic params for fetching fetchUrlpsqlQuery
#need to provide end point to fetch dispensary_ids and iteratite over all columns

def fetch_json(json_url):
    req = urllib.request.Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    return html

# fetch url to scrap
def fetchUrlpsqlQuery(columnName, table, dispensary_id):
    psql_select_Query = "select " + columnName + " from " + table + " where id = '" + dispensary_id + "';"
    return psql_select_Query

# Returns query and tuple of data to publish
def publishUrlJson(json_blob):
    uuid = random.randint(1000, 10000)
    psql_publish_Query = """ INSERT INTO json_blob (id, info) VALUES (%s, %s) """
    record_to_insert = (uuid, json_blob)
    print(uuid)
    return psql_publish_Query, record_to_insert

def connect():
    #TODO add dynamic params here
    columnName = "flower_url"
    table = "dispensaries"
    dispensary_id = "947808ec-f091-4507-bdc5-a1fb065f689d" 
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        #fetch url end point to grab json_blob
        url = fetchUrlpsqlQuery(columnName, table, dispensary_id)
        cur.execute(url)

        json_url = cur.fetchone()
        json_blob = fetch_json(json_url[0])
        publisher_data = publishUrlJson(json_blob)
        
        # Decode UTF-8 bytes to Unicode, and convert single quotes 
        # to double quotes to make it valid JSON
        byteToString = publisher_data[1][1].decode('utf8')#.replace("'", '"') # [1] == json_blob
        generatedId = str(publisher_data[1][0])
        record_to_insert = (generatedId, byteToString)
        query_to_run = publisher_data[0]
        cur.execute(query_to_run, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully")
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