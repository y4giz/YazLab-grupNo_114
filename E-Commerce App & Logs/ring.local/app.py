from flask import Flask, request, abort, jsonify, make_response, send_from_directory, render_template
from flask_cors import CORS, cross_origin
import uuid
import pymysql
import hashlib
import jwt
import numpy
import json
import ast
import requests
from datetime import datetime
import os

myApp = Flask(__name__)
CORS(myApp, resources={r"/*": {"origins": "*"}})  # Tüm kaynaklardan gelen isteklere izin verir

# Configure the database connection
myApp.config['MYSQL_HOST'] = ''
myApp.config['MYSQL_USER'] = ''
myApp.config['MYSQL_PASSWORD'] = ''
myApp.config['MYSQL_DB'] = ''
myApp.config['JWT_SECRET_KEY'] = '1234567890'
# JWT Secret is weak. Because we will try secret cracking

# Create a MySQL connection object
mysql = pymysql.connect(host=myApp.config['MYSQL_HOST'], 
                       user=myApp.config['MYSQL_USER'],
                       password=myApp.config['MYSQL_PASSWORD'],
                       db=myApp.config['MYSQL_DB'])
now = str(datetime.today())



LOG_DIR = "logs"  # Logların kaydedileceği dizin

def log_request(req):
    method = req.method
    method_dir = os.path.join(LOG_DIR, method)
    
    if not os.path.exists(method_dir):
        os.makedirs(method_dir)
    
    # Mevcut dosyaların sayısını al ve yeni bir dosya oluştur
    log_files = os.listdir(method_dir)
    log_number = len(log_files) + 1
    log_file = os.path.join(method_dir, f"{log_number}.json")
    
    # İstek bilgilerini JSON formatında logla
    log_data = {
        "method": method,
        "url": req.path,
        "headers": dict(req.headers),
        "data": req.data.decode('utf-8') if req.data else '',
        "timestamp": datetime.now().isoformat()  # ISO formatında zaman damgası
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

# Middleware
@myApp.before_request
def before_request_logging():
    log_request(request)

@myApp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@myApp.route('/<path:dosya_yolu>')
def sunucu_dosya(dosya_yolu):
    # Sunucu dosya yolu
    return send_from_directory('templates', dosya_yolu)

# HTML Routers
@myApp.route('/')
def shop():
   return render_template("shop.html")

    
@myApp.route('/register', methods=['POST'])
def register():
    # Get the user's information from the request body
    username = request.json.get('username', None)
    password = request.json.get('pass', None)
    password2 = request.json.get('pass2', None)
    email = request.json.get('email', None)
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname', None)

    # Validate the user's information
    if not all([username, password, password2, email, firstname, lastname]):
        return jsonify(message="Please provide a all datas"), 400
    # Validate passwords matches
    if password != password2:
        return jsonify(message="Passwords are not match"), 400
    
    # hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    # Insert the new user into the database
    try:
        new_user_id = str(uuid.uuid4())
        cursor = mysql.cursor()
        cursor.execute("INSERT INTO users (user_id, user_firstname, user_lastname, user_username, user_email, user_password_hash, user_role) VALUES (%s, %s, %s, %s, %s, %s, 0)", (new_user_id, firstname, lastname, username, email, hashed_password))
        mysql.commit()
        cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (new_user_id))
        mysql.commit()
        if cursor.fetchall():
            cursor.execute("INSERT INTO wallet (user_id, balance) VALUES (%s,'0')", (new_user_id))
            mysql.commit()
            return jsonify(message="User successfully registered"), 200
        else:
            return jsonify(message="Error while trying to register"), 400
    except pymysql.err.IntegrityError:
        return jsonify(message="This username or email has already been registered"), 400
    except pymysql.err.OperationalError:
        return jsonify(message="Database connection error"), 500

@myApp.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request body
    username = request.json.get('username', None)
    password = request.json.get('pass', None)
    if not all([username, password]):
        return jsonify(message="Please provide username and password"), 400
    # Query the database to check if the user exists
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM users WHERE user_username=%s AND user_password_hash=%s", (username, hashed_password))
    user = cursor.fetchone()
    if user is not None:
        # User exists and provided correct password
        access_token = create_access_token(identity=username)
        return jsonify(message='Successfully logged in', token=access_token), 200
    else:
        # User does not exist or provided incorrect password
        return jsonify(message="Invalid credentials"), 401

@myApp.route('/profile/info', methods=['GET', 'POST'])
def getProfile():
    if request.method == 'GET':
        try:
            username_parameter = request.args.get("username")
            username = ""
            if not username_parameter:
                username = getUsernameFromJWT()
            else:
                username = username_parameter
            cursor = mysql.cursor()
            cursor.execute("SELECT user_username, user_firstname, user_lastname, user_email, user_password_hash FROM users WHERE user_username=%s", (username))
            user = cursor.fetchone()
            if user:
                profile_info = {"username":user[0], "firstname": user[1], "lastname": user[2], "email": user[3], "password_hash": user[4]} 
                return jsonify(profile_info), 200
            else:
                return jsonify(message='User not found'), 400
        except jwt.exceptions.InvalidSignatureError:
            return jsonify(message='JWT Signature Error'), 500
        except jwt.exceptions.DecodeError:
            return jsonify(message='JWT Decode Error'), 500
    elif request.method == 'POST':
        username = getUsernameFromJWT()
        user = getUserID(username)
        if user:
            email = request.json.get('email', None)
            firstname = request.json.get('firstname', None)
            lastname = request.json.get('lastname', None)
            pass1 = request.json.get('pass', None)
            pass2 = request.json.get('pass2', None)
            if email and firstname and lastname:
                cursor = mysql.cursor()
                cursor.execute("SELECT user_email, user_id FROM users WHERE user_email=%s", (email))
                checkEmail = cursor.fetchone()
                if checkEmail and checkEmail[1] != user[0]:
                    return jsonify(message="This e-mail has already been registered"), 400
                elif pass1 != pass2:
                    return jsonify(message="Passwords are not matched"), 400
                else:
                    if pass1 != "" and pass2 != "":
                        hashed_password = hashlib.md5(pass1.encode()).hexdigest()
                        cursor = mysql.cursor()
                        user_pass_update = cursor.execute("UPDATE users SET user_firstname=%s, user_lastname=%s, user_email=%s, user_password_hash=%s WHERE user_id=%s", (firstname, lastname, email, hashed_password, user[0]))
                        mysql.commit()
                        if user_pass_update == 1:
                            return jsonify(message="User password succesfully updated"), 200
                        else:
                            return jsonify(message="User password couldn't update"), 400
                    else:
                        cursor = mysql.cursor()
                        user_info_update = cursor.execute("UPDATE users SET user_firstname=%s, user_lastname=%s, user_email=%s WHERE user_id=%s", (firstname, lastname, email, user[0]))
                        mysql.commit()
                        if user_info_update == 1:
                            return jsonify(message="User info succesfully updated"), 200
                        else:
                            return jsonify(message="User info couldn't update"), 400
            else:
                return jsonify(message="All inputs must be fill"), 400
        else:
            return jsonify(message="Unauthorized access"), 401

@myApp.route('/categories', methods=['GET'])
def getCategories():
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    if categories:
        all_categories = {"categories":[{"category_id":category[0], "category_name": category[1]} for category in categories]}
        return jsonify(all_categories), 200
    else:
        return jsonify(message="No categories found"), 400

@myApp.route('/products/trandy', methods=['GET'])
def getTrandyProducts():
    cursor = mysql.cursor()
    cursor.execute("SELECT product_id, product_name, product_image, product_price FROM products WHERE product_istrandy=1")
    trandyProducts = cursor.fetchall()
    cursor.close()
    if trandyProducts:
        all_trandyProducts = {"trandy_products":[{"product_id":trandyProduct[0], "product_name": trandyProduct[1], "product_image": trandyProduct[2], "product_price": trandyProduct[3]} for trandyProduct in trandyProducts]}
        return jsonify(all_trandyProducts), 200
    else:
        return jsonify(message="No trandy products found"), 400

@myApp.route('/products/all', methods=['GET'])
def getProducts():
    cursor = mysql.cursor()
    cursor.execute("SELECT product_id, product_name, product_image, product_price FROM products")
    products = cursor.fetchall()
    cursor.close()
    if products:
        all_products = {"products":[{"product_id":product[0], "product_name": product[1], "product_image": product[2], "product_price": product[3]} for product in products]}
        return jsonify(all_products), 200
    else:
        return jsonify(message="No trandy products found"), 400

@myApp.route('/search/<string:name>', methods=['GET'])
def getProduct(name):
    cursor = mysql.cursor()
    cursor.execute("SELECT product_id, product_name, product_image, product_price FROM products WHERE product_name LIKE %s", ('%' + name + '%'))
    products = cursor.fetchall()
    cursor.close()
    if products:
        all_products = {"products":[{"product_id":product[0], "product_name": product[1], "product_image": product[2], "product_price": product[3]} for product in products]}
        return jsonify(all_products), 200
    else:
        return jsonify(message="No product with "+name+" in it was found."), 400

@myApp.route("/product/<string:product_id>", methods=['GET'])
def getProductDetails(product_id):
    cursor = mysql.cursor()
    cursor.execute("SELECT product_id, product_name, product_image, product_price, product_description FROM products WHERE product_id='"+product_id+"'")
    product = cursor.fetchone()
    cursor.close()
    if product:
        product_detail = {"product_id":product[0], "product_name": product[1], "product_image": product[2], "product_price": product[3], "product_description": product[4]} 
        return jsonify(product_detail), 200
    else:
        return jsonify(message="Product not found"), 400    

@myApp.route("/contact", methods=['POST'])
def getContact():
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    subject = request.json.get('subject', None)
    message = request.json.get('message', None)

    if not all([name, email, subject, message]):
        return jsonify(message="Please provide a all datas"), 400
    cursor = mysql.cursor()
    new_contact_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO contacts (contact_id, contact_name, contact_email, contact_subject, contact_message) VALUES (%s, %s, %s, %s, %s)", (new_contact_id, name, email, subject, message))
    mysql.commit()
    cursor.execute("SELECT contact_id FROM contacts WHERE contact_id=%s", (new_contact_id))
    if cursor.fetchone():
        return jsonify(message="Your message delivered succesfully"), 200
    else:
        return jsonify(message="Error while trying to send message"), 400

@myApp.route("/profile/wallet", methods=['GET'])
def getBalance():
    try:
        username = getUsernameFromJWT()
        cursor = mysql.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_username=%s", (username))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT wallet_id, user_id, balance FROM wallet WHERE user_id=%s", (user[0]))
            wallet = cursor.fetchone()
            mysql.commit()
            wallet_detail = {"wallet_id":wallet[0], "user_id": wallet[1], "balance": wallet[2]} 
            return jsonify(wallet_detail), 200
        else:
            return jsonify(message='User not found'), 400
    except jwt.exceptions.InvalidSignatureError:
        return jsonify(message='JWT Signature Error'), 500
    except jwt.exceptions.DecodeError:
        return jsonify(message='JWT Decode Error'), 500

@myApp.route('/profile/deposit', methods=['POST'])
def deposit():
    try:
        value = request.json.get('deposit', None)
        cardnumber = request.json.get('cardnumber', None)
        date = request.json.get('date', None)
        cvc = request.json.get('cvc', None)

        if not all([value, cardnumber, date, cvc]):
            return jsonify(message="Please provide a all datas"), 400

        if float(value) < 0:
            return jsonify(message="Deposit value should bigger than 0"), 400

        if value.isdigit() != True or len(cardnumber) != 16:
            return jsonify(message="Please enter the credit card number correctly."), 400

        if '/' not in date or len(date) != 5:
            return jsonify(message="Please enter the date correctly."), 400

        if cvc.isdigit() != True or len(cvc) != 3:
            return jsonify(message="Please enter the CVC correctly."), 400

        username = getUsernameFromJWT()
        cursor = mysql.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_username=%s", (username))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT wallet_id, user_id, balance FROM wallet WHERE user_id=%s", (user[0]))
            mysql.commit()
            wallet = cursor.fetchone()
            new_balance = float(value) + float(wallet[2])
            cursor.execute("UPDATE wallet SET balance=%s WHERE wallet_id=%s", (str(new_balance), wallet[0]))
            mysql.commit()
            return jsonify(message='Balance succesfully updated'), 200
        else:
            return jsonify(message='User not found'), 400
    except:
        pass

@myApp.route('/basket', methods=['GET', 'POST', 'DELETE'])  
def basketOperations():
    username = getUsernameFromJWT()
    user = getUserID(username)
    if request.method == 'POST':
        product_id = request.json.get('product_id', None)
        quantity = request.json.get('quantity', None)
        image_path = request.json.get('image_path', None)
        if user:
            cursor = mysql.cursor()
            cursor.execute("SELECT basket_id, user_id, orders, basket_status FROM baskets WHERE user_id=%s AND basket_status=0", (user[0]))
            r = requests.get(url = image_path)
            basket = cursor.fetchone()
            if basket:
                orders_array = ast.literal_eval(basket[2])
                tmp_array = [str(product_id), quantity, calcProductTotal(product_id, quantity)]
                orders_array.append(tmp_array)
                orders = str(orders_array)
                cursor.execute("UPDATE baskets SET orders=%s WHERE basket_id=%s", (orders, basket[0]))
                mysql.commit()
                return jsonify(message='Product added'), 200
            else:
                orders_array = []
                orders_array.append([str(product_id), quantity, calcProductTotal(product_id, quantity)])
                orders = str(orders_array)
                now = str(datetime.today().strftime('%d-%m-%Y %H:%M'))
                cursor.execute("INSERT INTO baskets (user_id, orders, basket_status, basket_total, basket_date) VALUES (%s, %s, 0, 0, %s)", (user[0], orders, now))
                mysql.commit()
                return jsonify(message='Product added'), 200
    elif request.method == 'GET':
        if user:
            cursor = mysql.cursor()
            cursor.execute("SELECT basket_id, user_id, orders, basket_status FROM baskets WHERE user_id=%s AND basket_status=0", (user[0]))
            basket = cursor.fetchone()
            if basket:
                orders_array = numpy.array(ast.literal_eval(basket[2]))
                products_in_basket = {"products_in_basket":[{"product_id":orders_array[i][0], "product_name":getProductName(orders_array[i][0]), "product_quantity": orders_array[i][1], "total": orders_array[i][2], "product_image": getProductImage(orders_array[i][0])} for i in range(0, len(orders_array))]}
                return jsonify(products_in_basket), 200
            else:
                return jsonify(message='Product not found in basket'), 400        

@myApp.route('/basket/clear', methods=['GET'])
def clearBasket():
    username = getUsernameFromJWT()
    user = getUserID(username)
    if user:
            cursor = mysql.cursor()
            cursor.execute("DELETE FROM baskets WHERE user_id=%s AND basket_status=0", (user[0]))
            mysql.commit()
            cursor.execute("SELECT basket_id, user_id, orders, basket_status FROM baskets WHERE user_id=%s AND basket_status=0", (user[0]))
            mysql.commit()
            basket = cursor.fetchone()
            if basket:
                return jsonify(message="The basket could not be emptied."), 400
            else:
                return jsonify(message="The basket has been emptied."), 200

@myApp.route('/buy', methods=['POST'])
def buy():
    total = request.json.get('total', None)
    username = getUsernameFromJWT()
    user = getUserID(username)
    if user:
            cursor = mysql.cursor()
            cursor.execute("SELECT basket_id, user_id, orders, basket_status FROM baskets WHERE user_id=%s AND basket_status=0", (user[0]))
            mysql.commit()
            basket = cursor.fetchone()
            if basket:
                    basket_id = basket[0]
                    cursor = mysql.cursor()
                    cursor.execute("SELECT balance FROM wallet WHERE user_id=%s", (user[0]))
                    mysql.commit()
                    wallet = cursor.fetchone()
                    balance = float(wallet[0])
                    total = float(total)
                    if balance >= total:
                        new_balance = balance - total
                        cursor.execute("UPDATE wallet SET balance=%s WHERE user_id=%s", (str(new_balance), user[0]))
                        mysql.commit()
                        now = str(datetime.today().strftime('%d-%m-%Y %H:%M'))
                        cursor.execute("UPDATE baskets SET basket_status=1, basket_total=%s, basket_date=%s WHERE basket_id=%s", (str(total), now, int(basket_id)))
                        mysql.commit()
                        return jsonify(message="Your order has been received."), 200
                    else:
                        return jsonify(message="Insufficient balance."), 400
            else:
                return jsonify(message="Your basket is empty."), 400
    else:
        return jsonify(message="Unauthorized access"), 401

@myApp.route('/orders', methods=['GET'])
def getOrders():
    username = getUsernameFromJWT()
    user = getUserID(username)
    if user:
        cursor = mysql.cursor()
        cursor.execute("SELECT basket_id, user_id, orders, basket_status, basket_total, basket_date FROM baskets WHERE user_id=%s AND basket_status=1", (user[0]))
        mysql.commit()
        orders = cursor.fetchall()
        if orders:
            my_orders = {"my_orders":[{"order_id":order[0], "order_total":order[4], "order_detail": getOrderDetailsAsJSON(order[2]), "order_date": order[5]} for order in orders]}
            return jsonify(my_orders), 200

@myApp.route('/order/<int:order_id>', methods=['GET'])
def getOrderDetail(order_id):
    username = getUsernameFromJWT()
    user = getUserID(username)
    if user:
        cursor = mysql.cursor()
        cursor.execute("SELECT basket_id, user_id, orders, basket_status, basket_total, basket_date FROM baskets WHERE basket_id=%s AND basket_status=1", (order_id))
        mysql.commit()
        orderDetail = cursor.fetchone()
        if orderDetail:
            my_order = {"order":[{"order_id":orderDetail[0], "orderer": getOrdererInfo(orderDetail[1]), "order_detail": getOrderDetailsAsJSON(orderDetail[2]), "order_date": orderDetail[5], "order_total": orderDetail[4]}]}
            return jsonify(my_order), 200
        else:
           return jsonify(message="Order not found"), 400
    else:
        return jsonify(message="Unauthorized access"), 401

@myApp.route('/address/<string:username>', methods=['GET', 'POST'])
def address(username):
    if request.method == 'POST':
        user = getUserID(username)
        if user:
            address_header = request.json.get('address_header', None)
            address_content = request.json.get('address_content', None)

            if address_header and address_content:
                cursor = mysql.cursor()
                cursor.execute("SELECT address_id FROM addresses WHERE user_id=%s", (user[0]))
                mysql.commit()
                check_address = cursor.fetchone()
                if check_address:
                    cursor.execute("UPDATE addresses SET address_header=%s, address=%s WHERE user_id=%s", (address_header, address_content, user[0]))
                    mysql.commit()
                    return jsonify(message="Address updated."), 200
                else:
                    cursor.execute("INSERT INTO addresses (user_id, address_header, address) VALUES (%s, %s, %s)", (user[0], address_header, address_content))
                    mysql.commit()
                    return jsonify(message="Address added."), 200
            else:
                return jsonify(message="Your inputs can be empty. Please check that."), 400
        else:
            return jsonify(message="User not found"), 401
    elif request.method == 'GET':
        user = getUserID(username)
        if user:
            cursor = mysql.cursor()
            cursor.execute("SELECT address_header, address FROM addresses WHERE user_id=%s", (user[0]))
            mysql.commit()
            address_content = cursor.fetchone()
            if address_content:
                json_address = {"address_header":address_content[0], "address":address_content[1]}
                return jsonify(json_address), 200
            else:
                return jsonify(message="Address not found."), 400

@myApp.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == 'POST':
        name = request.json.get('name', None)
        subscriber_name = ""
        if name:
            subscriber_name = name
        email = request.json.get('email', None)
        if email:
            cursor = mysql.cursor()
            cursor.execute("SELECT subscriber_email FROM subscribers WHERE subscriber_email=%s", (email))
            mysql.commit()
            check_subscriber = cursor.fetchone()
            if check_subscriber:
                return jsonify(message="This email address is already subscribed"), 400
            else:
                new_subscriber_id = str(uuid.uuid4())
                cursor = mysql.cursor()
                cursor.execute("INSERT INTO subscribers (subscriber_id, subscriber_name, subscriber_email) VALUES (%s, %s, %s)", (new_subscriber_id, subscriber_name, email))
                mysql.commit()
                cursor.execute("SELECT subscriber_email FROM subscribers WHERE subscriber_email=%s", (email))
                mysql.commit()
                check = cursor.fetchone()
                if check:
                    return jsonify(message="This email successfully subscribed"), 200
                else:
                    return jsonify(message="This email couldn't subscribe"), 400
    elif request.method == 'GET':
        cursor = mysql.cursor()
        cursor.execute("SELECT subscriber_id, subscriber_name, subscriber_email FROM subscribers")
        mysql.commit()
        all_subscribers = cursor.fetchall()
        print(len(all_subscribers))
        if all_subscribers:
            json_subscriber = {"subscribers":[{"subscriber_id":subscriber[0], "subscriber_name":subscriber[1], "subscriber_email":subscriber[2]} for subscriber in all_subscribers]}
            return jsonify(json_subscriber), 200
        else:
            return jsonify(message="Subscribers couldn't be retrieved"), 400

@myApp.route('/forgotPassword/<string:username>', methods=['GET'])         
def forgotPassword(username):
    cursor = mysql.cursor()
    token = str(uuid.uuid4())
    cursor.execute("INSERT INTO reset_tokens (token, username, timestamp) VALUES (%s, %s, %s)", (token, username, now))
    mysql.commit()
    cursor.execute("SELECT token FROM reset_tokens WHERE token=%s", (token))
    mysql.commit()
    token_check = cursor.fetchone()
    if token_check:
        reset_token = {"reset_url": "new-password.html?token="+token}
        return jsonify(reset_token), 200
    else:
        return jsonify(message='A problem was encountered.'), 400

@myApp.route('/resetPassword/<string:token>', methods=['POST'])
def resetPassword(token):
    if not token or token == 'null':
        return jsonify(message='You should type your reset token'), 400
    else:
        password = request.json.get('pass', None)
        password2 = request.json.get('pass2', None)
        if password == password2:
            cursor = mysql.cursor()
            cursor.execute("SELECT username FROM reset_tokens WHERE token=%s", (str(token)))
            mysql.commit()
            token_check = cursor.fetchone()
            if token_check:
                username = token_check
                cursor = mysql.cursor()
                hashed_password = hashlib.md5(password.encode()).hexdigest()
                user_pass_update = cursor.execute("UPDATE users SET user_password_hash=%s WHERE user_username=%s", (hashed_password, username))
                mysql.commit()
                if user_pass_update == 1:
                    return jsonify(message='Password has been changed for user'), 200
                else:
                    return jsonify(message='A problem was encountered'), 400
            else:
                return jsonify(message='Token not found'), 400
        else:
            return jsonify(message='Passwords are not match'), 400

def create_access_token(identity):
    # Create a JWT token containing the user's identity
    encoded_token = jwt.encode({'identity': identity}, myApp.config['JWT_SECRET_KEY'] , algorithm='HS256')
    return encoded_token

def getUsernameFromJWT():
    access_token = request.headers.get('Authorization')
    if not access_token:
        return jsonify(message='Please login first'), 401
    decoded_token = jwt.decode(access_token, myApp.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    username = decoded_token['identity']
    return username

def getUserID(username):
    cursor = mysql.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_username=%s", (username))
    mysql.commit()
    user = cursor.fetchone()
    return user

def getOrdererInfo(user_id):
    cursor = mysql.cursor()
    cursor.execute("SELECT user_firstname, user_lastname, user_email FROM users WHERE user_id=%s", (user_id))
    mysql.commit()
    user = cursor.fetchone()
    return "Orderer: "+user[0]+" "+user[1]+" "+user[2]

def calcProductTotal(product_id, quantity):
    cursor = mysql.cursor()
    cursor.execute("SELECT product_price FROM products WHERE product_id=%s", (product_id))
    product = cursor.fetchone()
    if product:
        product_price = product[0]
        total = float(product_price) * int(quantity)
        return total

def getProductName(product_id):
    cursor = mysql.cursor()
    cursor.execute("SELECT product_name FROM products WHERE product_id=%s", (product_id))
    product = cursor.fetchone()
    if product:
        return product[0]

def getProductImage(product_id):
    cursor = mysql.cursor()
    cursor.execute("SELECT product_image FROM products WHERE product_id=%s", (product_id))
    product = cursor.fetchone()
    if product:
        return product[0]

def getOrderDetailsAsJSON(orders):
    orders_array = ast.literal_eval(orders)
    return_json = [{"product_name": getProductName(order_detail[0]), "quantity": order_detail[1], "total": order_detail[2]} for order_detail in orders_array]
    return return_json

if __name__ == '__main__':
    myApp.run(debug=1)
    myApp.run(host='0.0.0.0')
