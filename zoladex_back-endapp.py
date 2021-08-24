import hmac
import sqlite3
import datetime

from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from flask_mail import Mail


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


def init_user_register_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS user_register(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL,"
                 "address TEXT NOT NULL,"
                 "phone TEXT NOT NULL,"
                 "email TEXT NOT NULL)")
    print("user table created successfully")
    conn.close()


def init_brand_register_table():
    conn = sqlite3.connect('Zoladex.db')
    print("Opened database successfully")

    conn.execute("CREATE TABLE IF NOT EXISTS zoladex_brand_application(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "ceo_name TEXT NOT NULL,"
                 "ceo_surname TEXT NOT NULL,"
                 "brand_name TEXT NOT NULL,"
                 "brand_registration_number TEXT NOT NULL,"
                 "brand_style TEXT NOT NULL,"
                 "social_media_link TEXT NOT NULL,"
                 "office_address TEXT NOT NULL,"
                 "brand_phone TEXT NOT NULL,"
                 "brand_email TEXT NOT NULL)")
    print("brands table created successfully")
    conn.close()


init_user_register_table()
init_brand_register_table()

app = Flask(__name__)


@app.route('/create-blog/', methods=["POST"])
@cross_origin()
def create_blog():
    response = {}

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        date_created = datetime.datetime.now()

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


@app.route('/brand-registration/', methods=["POST"])
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


@app.route('/user-registration/', methods=["POST"])
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

        with sqlite3.connect("Zoladex.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user_register("
                           "first_name,"
                           "last_name,"
                           "username,"
                           "password,"
                           "address,"
                           "phone,"
                           "email) VALUES(?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, username, password, address, phone, email))
            conn.commit()
            response["message"] = "success"
            response["status_code"] = 201

            # msg = Message('WELCOME', sender='sithandathuzipho@gmail.com', recipients=['sithandathuzipho@gmail.com'])
            # msg.body = "You have successfully registered"
            # mail.send(msg)
        return response


if __name__ == '__main__':
    app.run(debug=True)