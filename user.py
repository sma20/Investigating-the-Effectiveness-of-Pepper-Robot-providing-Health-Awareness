# ===========
#   Imports
# ===========
import sqlite3 as sql
import os


# ==================================
#  Insert data in database (SIGNUP)
# ==================================
def insertUser(name, age, allergies, health, image):
    con = sql.connect("db/app.db")
    cur = con.cursor()
    query = ("""INSERT INTO USERS
             (name,age,allergies,health,image)
             VALUES ('%s', '%s', '%s', '%s', '%s')""" %
             (name, age, allergies, health, image))

    print(query)
    cur.execute(query)
    con.commit()
    con.close()


def getUser(filename):

    con = sql.connect("db/app.db")
    cur = con.cursor()
    query = ("SELECT name, health, allergies, id FROM USERS WHERE image = 'captures/"+filename+"'")
    cur.execute(query)
    rv = cur.fetchall()
    con.commit()
    con.close()
    return rv



def addFood(name, image, user, today):

    con = sql.connect("db/app.db")
    cur = con.cursor()
    query = ("""INSERT INTO FOOD
             (userID,name,image,data)
             VALUES ('%s', '%s', '%s', '%s')""" %
             (user, name, image, today))



    cur.execute(query)
    con.commit()
    con.close()

def getFood(user):

    con = sql.connect("db/app.db")
    cur = con.cursor()
    query = ("SELECT userID,name,image,data FROM FOOD WHERE userID = "+str(user))
    cur.execute(query)
    rv = cur.fetchall()
    con.commit()
    con.close()
    return rv
