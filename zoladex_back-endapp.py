import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from smtplib import SMTPRecipientsRefused, SMTPAuthenticationError


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def init_user_register_table():
    conn = sqlite3.connect('Zoladex.db')
    # print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user_registration(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "address TEXT NOT NULL,"
                 "phone TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "datetime)")
    print("user table created successfully")
    conn.close()


# creating a login table
def init_user_login_table():
    with sqlite3.connect('Zoladex.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS user_login (user_login_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "user_email TEXT NOT NULL,"
                     "password TEXT NOT NULL,"
                     "login_date TEXT NOT NULL,"
                     "CONSTRAINT fk_user FOREIGN KEY (user_email) REFERENCES user_registration(user_id))")
    print("Login table created successfully.")


def init_brand_register_table():
    conn = sqlite3.connect('Zoladex.db')
    # print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS zoladex_brand_application(brand_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "ceo_name TEXT NOT NULL,"
                 "ceo_surname TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "brand_registration_number TEXT NOT NULL,"
                 "brand_style TEXT NOT NULL,"
                 "social_media_link TEXT NOT NULL,"
                 "office_address TEXT NOT NULL,"
                 "brand_phone TEXT NOT NULL,"
                 "brand_email TEXT NOT NULL,"
                 "datetime)")
    print("brands table created successfully")
    conn.close()

def init_brand_products_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS brand_products(brand_product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "user_id INTEGER"
                 "price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "CONSTRAINT fk_product FOREIGN KEY (user_id) REFERENCES user_registration(user_id))")
    print("brand_products table created successfully")
    conn.close()

def init_order_products_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS order_product(order_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL)")
    print("order_products table created successfully")
    conn.close()


init_brand_products_table()
init_order_products_table()
init_user_register_table()
init_user_login_table()
init_brand_register_table()


app = Flask(__name__)


@app.route('/create-blog/', methods=["POST"])
@cross_origin()
def create_blog():
    response = {}

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        date_created = datetime.now()

        with sqlite3.connect('Zoladex.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO post("
                           "title,"
                           "content,"
                           "date_created) VALUES(?, ?, ?)", (title, content, date_created))
            conn.commit()
            response["status_code"] = 201
            response['description'] = "Blog post added successfully"
        return response


@app.route('/brand-registration/', methods=["POST", "GET"])
@cross_origin()
def brand_registration():
    response = {}
    if request.method == "POST":

        ceo_name = request.form['ceo_name']
        ceo_surname = request.form['ceo_surname']
        brand_name = request.form['brand_name']
        brand_registration_number = request.form['brand_registration_number']
        brand_style = request.form['brand_style']
        social_media_link = request.form['social_media_link']
        office_address = request.form['office_address']
        brand_phone = request.form['brand_phone']
        brand_email = request.form['brand_email']

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO zoladex_brand_application("
                           "ceo_name,"
                           "ceo_surname,"
                           "brand_name,"
                           "brand_registration_number,"
                           "brand_style,"
                           "social_media_link,"
                           "office_address,"
                           "brand_phone,"
                           "brand_email) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (ceo_name, ceo_surname, brand_name, brand_registration_number, brand_style, social_media_link, office_address, brand_phone, brand_email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

            # msg = Message('WELCOME', sender='sithandathuzipho@gmail.com', recipients=['sithandathuzipho@gmail.com'])
            # msg.body = "You have successfully registered"
            # mail.send(msg)
        return response
    if request.method == "GET":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM zoladex_brand_application")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/user-registration/', methods=["POST", "GET"])
@cross_origin()
def user_registration():

    response = {}
    if request.method == "POST":

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        today_date = datetime.datetime.now()

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_registration("
                           "first_name,"
                           "last_name,"
                           "username,"
                           "password,"
                           "address,"
                           "phone,"
                           "email,"
                           "datetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, username, password, address, phone, email, today_date))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

            # msg = Message('WELCOME', sender='sithandathuzipho@gmail.com', recipients=['sithandathuzipho@gmail.com'])
            # msg.body = "You have successfully registered"
            # mail.send(msg)
        return response

    if request.method == "GET":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM user_register")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/user-login/', methods=["POST"])
@cross_origin()
def user_login():
    response = {}
    if request.method == "POST":
        try:

            user_email = request.form['user_email']
            password = request.form['password']
            date_created = datetime.datetime.now()

            with sqlite3.connect("Zoladex.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user_login("
                               "user_email,"
                               "password,"
                               "login_date) VALUES(?, ?, ?)", (user_email, password, date_created))
                conn.commit()
                response["message"] = "success"
                response["status_code"] = 201

                return response
        except SMTPRecipientsRefused:
            response["message"] = "Invalid email used"
            response["status_code"] = 401
            return response
        except SMTPAuthenticationError:
            response["message"] = "Incorrect login details"
            response["status_code"] = 401
            return response


@app.route('/brand-products/', methods=["POST", "GET"])
@cross_origin()
def brand_products():
    response = {}
    if request.method == "POST":

        product_tittle = request.form['product_tittle']
        brand_name = request.form['brand_name']
        image = request.form['image']
        price = request.form['price']
        size = request.form['size']
        colour = request.form['colour']
        description = request.form['description']

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO brand_products("
                           "product_tittle,"
                           "brand_name,"
                           "image,"
                           "price,"
                           "size,"
                           "colour,"
                           "description) VALUES(?, ?, ?, ?, ?, ?, ?)", (product_tittle, brand_name, image, price, size, colour, description))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

            # msg = Message('WELCOME', sender='sithandathuzipho@gmail.com', recipients=['sithandathuzipho@gmail.com'])
            # msg.body = "You have successfully registered"
            # mail.send(msg)
        return response

    if request.method == "GET":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM brand_products")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/order-products/', methods=["POST", "GET"])
@cross_origin()
def order_products():
    # response = {}
    # if request.method == "POST":
    #
    #     product_tittle = request.form['product_tittle']
    #     brand_name = request.form['brand_name']
    #     image = request.form['image']
    #     price = request.form['price']
    #     size = request.form['size']
    #     colour = request.form['colour']
    #     description = request.form['description']
    #
    #     with sqlite3.connect("Zoladex.db") as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("INSERT INTO order_products("
    #                        "product_tittle,"
    #                        "brand_name,"
    #                        "image,"
    #                        "price,"
    #                        "size,"
    #                        "colour,"
    #                        "description) VALUES(?, ?, ?, ?, ?, ?, ?)", (product_tittle, brand_name, image,
    #                        price, size, colour, description))
    #         conn.commit()
    #         response["message"] = "success"
    #         response["status_code"] = 201
    #
    #         # msg = Message('WELCOME', sender='sithandathuzipho@gmail.com', recipients=['sithandathuzipho@gmail.com'])
    #         # msg.body = "You have successfully registered"
    #         # mail.send(msg)
    #     return response

    if request.method == "GET":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM brand_products")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


if __name__ == '__main__':
    app.run(debug=True)