#!/usr/bin/python
import psycopg2
import json
import sys
import uuid
from config import config
from psycopg2 import connect, Error
#$python3 new_company.py <company_name>
def connect():
    # total arguments
    n = len(sys.argv)
    print("Total arguments passed:", n)

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        print ("\ncreated cursor object:", cur)

        # generate UUID for company ID, int has no subscriptable and must be short enough for DB
        id = str(uuid.uuid4())
        company_name = sys.argv[1]

        # insert data
        postgres_insert_query = """ INSERT INTO companies (id, company_name) VALUES (%s, %s)"""
        record_to_insert = (id, company_name)
        cur.execute(postgres_insert_query, record_to_insert)
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

if __name__ == "__main__":
    connect()