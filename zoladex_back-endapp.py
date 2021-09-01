import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from flask_mail import Mail
from smtplib import SMTPRecipientsRefused, SMTPAuthenticationError


class User(object):
    def __init__(self, user_id, first_name, last_name, username, password, address, phone, email):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone
        self.email = email


# user registration
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
                     "login_date,"
                     "CONSTRAINT fk_user FOREIGN KEY (user_email) REFERENCES user_registration(user_id))")
    print("Login table created successfully.")


# brand registration table
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


# brand table
def init_brand_products_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS brand_products(product_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "user_id INTEGER,"
                 "price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "CONSTRAINT fk_product FOREIGN KEY (user_id) REFERENCES user_registration(user_id))")
    print("brand_products table created successfully")
    conn.close()


# order table
def init_order_products_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS order_product(order_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "order_no TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "order_date TEXT NOT NULL,"
                 "CONSTRAINT fk_order FOREIGN KEY (product_tittle) REFERENCES brand_products(product_id))")
    print("order_products table created successfully")
    conn.close()


# Products table
def init_products_cart_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS product_cart(cart_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "cart_date,"
                 "CONSTRAINT fk_cart FOREIGN KEY (product_tittle) REFERENCES brand_products(product_id) )")
    print("product_cart table created successfully")
    conn.close()


# checkout table
def init_checkout_products_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS checkout_product(cart_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "product_tittle TEXT NOT NULL,"
                 "order_no TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "image TEXT NOT NULL,"
                 "total_price TEXT NOT NULL,"
                 "size TEXT NOT NULL,"
                 "colour TEXT NOT NULL,"
                 "description TEXT NOT NULL,"
                 "checkout_date,"
                 "CONSTRAINT fk_checkouts FOREIGN KEY (order_no) REFERENCES brand_products (order_no))")
    print("checkouts table created successfully")
    conn.close()


# Payment table
def init_payment_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS payment(payment_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "cardholder_name TEXT NOT NULL,"
                 "card_number TEXT NOT NULL,"
                 "order_no TEXT NOT NULL,"
                 "end_date TEXT NOT NULL,"
                 "cvv TEXT NOT NULL,"
                 "payment_method TEXT NOT NULL,"
                 "payment_date TEXT NOT NULL,"
                 "CONSTRAINT fk_payment FOREIGN KEY (order_no) REFERENCES brand_products(product_id))")
    print("payment table created successfully")
    conn.close()


# Shipping table
def shipping_address():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS products_shipping(ship_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "buyers_fullname TEXT NOT NULL,"
                 "order_no TEXT NOT NULL,"
                 "brand TEXT NOT NULL,"
                 "buyers_address TEXT NOT NULL,"
                 "city TEXT NOT NULL,"
                 "country TEXT NOT NULL,"
                 "province TEXT NOT NULL,"
                 "postal_code TEXT NOT NULL,"
                 "recipient_phone TEXT NOT NUll,"
                 "data TEXT NOT NULL,"
                 "FOREIGN KEY(order_no) REFERENCES order_product(order_id))")
    print("shipping table created successfully")
    conn.close()


# User contact table
def init_contact_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS contact(client_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "fullname TEXT NOT NULL,"
                 "email TEXT NOT NULL,"
                 "regarding TEXT NOT NULL,"
                 "order_no TEXT NOT NULL,"
                 "questions TEXT NOT NULL,"
                 "message TEXT NOT NULL,"
                 "contact_date,"
                 "CONSTRAINT fk_contact FOREIGN KEY (fullname) REFERENCES user_registration (user_id))")
    print("contacts table created successfully")
    conn.close()


# My closed functions
init_payment_table()
init_contact_table()
init_products_cart_table()
init_brand_products_table()
init_order_products_table()
init_user_register_table()
init_user_login_table()
init_brand_register_table()


def fetch_users():
    with sqlite3.connect('Zoladex.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_registration")
        users = cursor.fetchall()
        new_data = []
        for data in users:
            new_data.append(User(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    return new_data


users = fetch_users()


email_table = {u.email: u for u in users}
user_id_table = {u.user_id: u for u in users}


def authenticate(email, password):
    user = email_table.get(email, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_id_table.get(user_id, None)


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
# @jwt_required()
@cross_origin()
def protected():
    return '%s' % current_identity


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
            cursor.execute("SELECT * FROM user_registration")
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


@app.route('/products_cart/', methods=["POST", "GET"])
@cross_origin()
def products_cart():
    response = {}
    if request.method == "GET":
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

    if request.method == "POST":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("INSERT INTO product_cart")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/checkouts/', methods=["POST", "GET"])
@cross_origin()
def checkouts():
    response = {}
    if request.method == "Post":
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM product_cart")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response

    if request.method == "GET":
        response = {}
        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("INSERT INTO checkout_products")
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


@app.route('/payment/', methods=["POST", "GET"])
@cross_origin()
def payment():
    response = {}
    if request.method == "POST":

        cardholder_name = request.form['cardholder_name']
        card_number = request.form['card_number']
        order_no = request.form['order_no']
        end_date = request.form['end_date']
        cvv = request.form['cvv']
        payment_method = request.form['payment_method']
        payment_date = request.form['payment_date']
        province = request.form['province']
        postal_code = request.form['postal_code']
        recipient_phone = request.form['recipient_phone']
        paymnet_date = datetime.datetime.now()

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO payment("
                           "cardholder_name,"
                           "card_number,"
                           "order_no,"
                           "end_date,"
                           "cvv,"
                           "payment_method,"
                           "payment_date) VALUES(?, ?, ?, ?, ?, ?, ?)", (cardholder_name, card_number, order_no, end_date, cvv, payment_method, payment_date))
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
            cursor.execute("SELECT * FROM payment")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/shipment/', methods=["POST", "GET"])
@cross_origin()
def shipping():
    response = {}
    if request.method == "POST":

        buyers_fullname = request.form['buyers_fullname']
        order_no = request.form['order_no']
        brand = request.form['brand']
        buyers_address = request.form['buyers_address']
        city = request.form['city']
        country = request.form['country']
        province = request.form['province']
        postal_code = request.form['postal_code']
        recipient_phone = request.form['recipient_phone']
        date = datetime.datetime.now()

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO shipping("
                           "buyers_fullname,"
                           "order_no,"
                           "brand,"
                           "buyers_address,"
                           "city,"
                           "country,"
                           "province,"
                           "postal_code,"
                           "recipient_phone,"
                           "date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (buyers_fullname, order_no, brand, buyers_address, city, country, province, postal_code, recipient_phone, date))
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
            cursor.execute("SELECT * FROM shipping")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


@app.route('/contact-us/', methods=["POST", "GET"])
@cross_origin()
def contact_us():
    response = {}
    if request.method == "POST":

        fullname = request.form['fullname']
        email = request.form['email']
        regarding = request.form['regarding']
        order_no = request.form['order_no']
        questions = request.form['questions']
        message = request.form['message']
        date = datetime.datetime.now()

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contact("
                           "fullname,"
                           "email,"
                           "regarding,"
                           "order_no,"
                           "questions,"
                           "message,"
                           "date) VALUES(?, ?, ?, ?, ?, ?, ?)", (fullname, email, regarding, order_no, questions, message, date))
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
            cursor.execute("SELECT * FROM contact")
            deals = cursor.fetchall()
            deal_acc = []
            for i in deals:
                deal_acc.append({x: i[x] for x in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(deal_acc)
        return response


# delete user by id
@app.route("/delete-user/<int:post_id>", methods=['POST'])
@cross_origin()
# @jwt_required()
def delete_user(user_id):
    response = {}
    with sqlite3.connect("Zoladex.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_registration WHERE user_id=" + str(user_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "User deleted successfully."
    return response


# update single user
@app.route('/update-user/<int:user_id>/', methods=["PUT"])
@cross_origin()
# @jwt_required()
def edit_user(user_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('Zoladex.db') as conn:
            incoming_data = dict(request.json)

            put_data = {}

            if incoming_data.get("first_name") is not None:  # check if the updated column is price
                put_data["first_name"] = incoming_data.get("first_name")
                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET first_name =? WHERE user_id=?", (put_data["first_name"], user_id))
                    conn.commit()
                    response['message'] = "First name updated"
                    response['status_code'] = 200
            if incoming_data.get("last_name") is not None:
                put_data['last_name'] = incoming_data.get('last_name')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET last_name =? WHERE user_id=?", (put_data["last_name"], user_id))
                    conn.commit()

                    response["content"] = "Last name updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("username") is not None:
                put_data['username'] = incoming_data.get('username')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET username =? WHERE user_id=?", (put_data["username"], user_id))
                    conn.commit()

                    response["content"] = "Username updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("password") is not None:
                put_data['password'] = incoming_data.get('password')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET password =? WHERE user_id=?", (put_data["password"], user_id))
                    conn.commit()

                    response["content"] = "Password updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("address") is not None:
                put_data['address'] = incoming_data.get('address')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET address =? WHERE user_id=?", (put_data["address"], user_id))
                    conn.commit()

                    response["content"] = "Address updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("phone") is not None:
                put_data['phone'] = incoming_data.get('phone')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET phone =? WHERE user_id=?",
                                   (put_data["phone"], user_id))
                    conn.commit()

                    response["content"] = "Phone updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("email") is not None:
                put_data['email'] = incoming_data.get('email')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_registration SET email =? WHERE user_id=?", (put_data["email"], user_id))
                    conn.commit()

                    response["content"] = "Email updated successfully"
                    response["status_code"] = 200

    return response


# update product by id
@app.route('/update-product/<int:product_id>/', methods=["PUT"])
@cross_origin()
# @jwt_required()
def update_product(product_id):
    response = {}

    if request.method == "PUT":
        with sqlite3.connect('Zoladex.db') as conn:
            incoming_data = dict(request.json)

            put_data = {}

            if incoming_data.get("product_tittle") is not None:  # check if the updated column is price
                put_data["product_tittle"] = incoming_data.get("product_tittle")
                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET product_tittle =? WHERE product_id=?", (put_data["product_tittle"], product_id))
                    conn.commit()
                    response['message'] = "Product_tittle updated"
                    response['status_code'] = 200

            if incoming_data.get("brand_name") is not None:
                put_data['brand_name'] = incoming_data.get('brand_name')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET brand_name =? WHERE product_id=?",
                                   (put_data["brand_name"], product_id))
                    conn.commit()

                    response["content"] = "Brand name updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("image") is not None:
                put_data['image'] = incoming_data.get('image')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET image =? WHERE product_id=?", (put_data["image"], product_id))
                    conn.commit()

                    response["content"] = "Product image updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("user_id") is not None:
                put_data['user_id'] = incoming_data.get('user_id')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET user_id =? WHERE product_id=?", (put_data["user_id"], product_id))
                    conn.commit()

                    response["content"] = "User id updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("price") is not None:
                put_data['price'] = incoming_data.get('price')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET price =? WHERE product_id=?",
                                   (put_data["price"], product_id))
                    conn.commit()

                    response["content"] = "Price updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("size") is not None:
                put_data['size'] = incoming_data.get('size')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET size =? WHERE product_id=?",
                                   (put_data["size"], product_id))
                    conn.commit()

                    response["content"] = "Size updated successfully"
                    response["status_code"] = 200

            if incoming_data.get("colour") is not None:
                put_data['colour'] = incoming_data.get('colour')

                with sqlite3.connect('Zoladex.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE brand_products SET colour =? WHERE product_id=?", (put_data["colour"], product_id))
                    conn.commit()

                    response["content"] = "Colour updated successfully"
                    response["status_code"] = 200

    return response


# delete product by id
@app.route("/delete-product/<int:prod_id>", methods=['POST'])
@cross_origin()
# @jwt_required()
def delete_single_product(product_id):
    response = {}
    with sqlite3.connect("Zoladex.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM brand_products WHERE product_id=" + str(product_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product deleted successfully."
    return response


@app.route('/orders/', methods=["POST", "GET"])
@cross_origin()
# @jwt_required()
def orders_info():
    response = {}
    now = datetime.now()
    if request.method == "POST":
        try:
            product_image = request.json['product_image']
            order_number = request.json['order_number']
            product_name = request.json['product_name']
            total_price = request.json['total_price']
            product_quantity = request.json['product_quantity']

            with sqlite3.connect("Zoladex.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO orders_product("
                               "product_image,"
                               "order_date,"
                               "order_number,"
                               "product_name,"
                               "total_price,"
                               "product_quantity) VALUES(?, ?, ?, ?, ?, ?)",
                               (product_image, now, order_number, product_name, total_price, product_quantity))
                conn.commit()
                response["message"] = "Order added successfully "
                response["status_code"] = 201

                return response
        except Exception:
            response["message"] = "Enter correct order injsonation"
            response["status_code"] = 401
            return response
    if request.method == "GET":

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * FROM orders_product")
            posts = cursor.fetchall()
            accumulator = []

            for i in posts:
                accumulator.append({k: i[k] for k in i.keys()})

        response['status_code'] = 200
        response['data'] = tuple(accumulator)
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)