import mysql.connector
from mysql.connector import Error
import conf

def Select_price(name):
    try:
        con = mysql.connector.connect(host='localhost',
                                          database='testDB',
                                          user=conf.userDB,
                                          password=conf.pasDB)
        if con.is_connected():
                cursor = con.cursor()
                query = ("SELECT name, specifica, amount, link_photo from SHOP_POSITION where name='%s'" % (name))
                cursor.execute(query)
                result = cursor.fetchall()
        return result
    except Error as e:
            print(e)
    finally:
            con.close()


def Conncet():
    try:
        con = mysql.connector.connect(host='localhost',
                              database='testDB',
                              user=conf.userDB,
                              password=conf.pasDB)

        if con.is_connected():

            name_position = list()
            cursor = con.cursor()
            query = ("SELECT id,name from SHOP_POSITION")
            cursor.execute(query)

            for id,name in cursor:
                name_position.append(name)

        return name_position
    except Error as e:
        print(e)

    finally:
        con.close()