import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

request_category = "SELECT * FROM category"
request_cake = "SELECT * FROM offers WHERE offers.category_id=1"
request_bread = "SELECT * FROM offers WHERE offers.category_id=2"
request_pizza = "SELECT * FROM offers WHERE offers.category_id=3"
request_pie = "SELECT * FROM offers WHERE offers.category_id=4"


def sql_request_data(sqlite_request):
    res = cur.execute(sqlite_request)
    offers = res.fetchall()
    return offers
