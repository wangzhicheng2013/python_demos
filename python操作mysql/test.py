#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
db = MySQLdb.connect("localhost", "root", "123456", "mysql", charset='utf8' )
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print "Database version:%s" %data

db = MySQLdb.connect("localhost", "root", "123456", charset='utf8' )
cursor = db.cursor()
cursor.execute("CREATE DATABASE test1")
cursor.execute("SHOW DATABASES")
for x in cursor:
    print(x)
db.close()

