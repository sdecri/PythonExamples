__author__ = 'Simone'

import psycopg2
import sys


def writePersonOnDb(persons):
    conn=None
    try:
        conn = psycopg2.connect("dbname='python_test' user='postgres' host='localhost' password='postgres'")
        cursor=conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS persons"
        + "(name character varying(255), surname character varying(255), age integer) ")
        cursor.execute("TRUNCATE TABLE persons")
        # insert persons
        cursor.executemany("INSERT INTO persons (name, surname, age) VALUES (%s, %s, %s)", persons)
        conn.commit()
        print("Wrote on DB: " ,persons)
    except psycopg2.DatabaseError as e:
        if conn:
            conn.rollback()
        print ('Error %s' % e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()
