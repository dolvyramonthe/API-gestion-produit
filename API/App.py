import pymysql
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from config import DATABASE_CONFIG

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  #  clé secrète forte 
jwt = JWTManager(app)
mysql = pymysql.connect(**DATABASE_CONFIG)

def get_cursor():
    return mysql.cursor(pymysql.cursors.DictCursor)

# Routes pour les produits
@app.route("/products/create", methods=['POST'])
def create_product():
    try:
        _json = request.json
        _name = _json['name']
        _price = _json['price']
        _description = _json['description']
        _image_path = _json['image_path']
        _status = _json['status']

        if _name and _price and _description and _image_path and _status and request.method == 'POST':
            cursor = get_cursor()
            sql_query = "INSERT INTO products(name, price, description, image_path, status) VALUES(%s, %s, %s, %s, %s)"
            bind_data = (_name, _price, _description, _image_path, _status)
            cursor.execute(sql_query, bind_data)
            mysql.commit()
            response = jsonify('Product added successfully')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/products/update', methods=['PUT'])
def update_product():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _price = _json['price']
        _description = _json['description']
        _image_path = _json['image_path']
        _status = _json['status']

        if _name and _price and _description and _image_path and _status and _id and request.method == 'PUT':
            cursor = get_cursor()
            sql_query = "UPDATE products SET name=%s, price=%s, description=%s, image_path=%s, status=%s WHERE id=%s"
            bind_data = (_name, _price, _description, _image_path, _status, _id)
            cursor.execute(sql_query, bind_data)
            mysql.commit()
            response = jsonify('Product updated successfully')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/products', methods=['GET'])
def get_all_products():
    try:
        cursor = get_cursor()
        cursor.execute("SELECT id, name, price, description, image_path, status FROM products")
        products = cursor.fetchall()
        response = jsonify(products)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/products/<int:id>', methods=['GET', 'DELETE'])
def manage_product(id):
    cursor = get_cursor()
    if request.method == 'GET':
        try:
            cursor.execute("SELECT id, name, price, description, image_path, status FROM products WHERE id = %s", id)
            product = cursor.fetchone()
            if product:
                response = jsonify(product)
                response.status_code = 200
                return response
            else:
                return showMessage()
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    elif request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM products WHERE id = %s", id)
            mysql.commit()
            response = jsonify('Product deleted successfully')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()

# Routes pour les utilisateurs
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        cursor = get_cursor()
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()
        response = jsonify(users)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/users/create', methods=['POST'])
def create_user():
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']
        _email = _json['email']
        _role = _json.get('role', 'USER')  # Ajout du rôle avec la valeur par défaut 'USER'

        if _username and _password and _email and request.method == 'POST':
            cursor = get_cursor()
            sql_query = "INSERT INTO users(username, password, email, role) VALUES(%s, %s, %s, %s)"
            bind_data = (_username, _password, _email, _role)
            cursor.execute(sql_query, bind_data)
            mysql.commit()
            response = jsonify('User created successfully')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(id):
    cursor = get_cursor()
    if request.method == 'GET':
        try:
            cursor.execute("SELECT id, username, email, role FROM users WHERE id = %s", id)
            user = cursor.fetchone()
            if user:
                response = jsonify(user)
                response.status_code = 200
                return response
            else:
                return showMessage()
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    elif request.method == 'PUT':
        try:
            _json = request.json
            _username = _json['username']
            _password = _json['password']
            _email = _json['email']
            _role = _json.get('role', 'USER')  # Ajout du rôle avec la valeur par défaut 'USER'

            if _username and _password and _email and id and request.method == 'PUT':
                cursor = get_cursor()
                sql_query = "UPDATE users SET username=%s, password=%s, email=%s, role=%s WHERE id=%s"
                bind_data = (_username, _password, _email, _role, id)
                cursor.execute(sql_query, bind_data)
                mysql.commit()
                response = jsonify('User updated successfully')
                response.status_code = 200
                return response
            else:
                return showMessage()
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    elif request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", id)
            mysql.commit()
            response = jsonify('User deleted successfully')
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close()

# Route pour l'authentification
@app.route('/login', methods=['POST'])
def login():
    cursor = None
    try:
        _json = request.json
        _username = _json['username']
        _password = _json['password']

        cursor = get_cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s AND password = %s", (_username, _password))
        user = cursor.fetchone()

        if user:
            # Créez un token d'accès avec l'identifiant de l'utilisateur
            access_token = create_access_token(identity=user['id'])
            
            # Ajoutez le token à la table des tokens
            expiration_date = datetime.utcnow() + timedelta(hours=2)  # Par exemple, expire dans 2 heures
            cursor.execute("INSERT INTO tokens (user_id, token, expiration_date) VALUES (%s, %s, %s)",
                           (user['id'], access_token, expiration_date))
            mysql.commit()
            
            response = jsonify(access_token=access_token)
            response.status_code = 200
            return response
        else:
            # Authentification échouée, retournez une réponse JSON appropriée
            app.logger.warning(f"Failed login attempt for user: {_username}")
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred during login"}), 500
    finally:
        cursor.close()

# Fonction utilitaire pour gérer les erreurs 404
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)
