from flask import Flask, request, jsonify
import psycopg2
import os 
from werkzeug.security import generate_password_hash

app = Flask(__name__)

#setup pg db connection
conn = psycopg2.connect(
  dbname = 'flask_test_users',
  user= os.getenv('FLASK_DB_USER'),
  password= os.getenv('FLASK_DB_PASSWORD'),
  host= os.getenv('FLASK_DB_HOST'),
  port= os.getenv('FLASK_DB_PORT', '5432')
)

print("\n⚡ Connected to DB:", conn.get_dsn_parameters()['dbname'], "\n")

conn.autocommit = True
cur = conn.cursor()

def load_sql(function_name):
    file_path = os.path.join("db", "queries", "users_queries.sql")
    with open(file_path, "r") as file:
        content = file.read()

    import re
    match = re.search(
        rf"def {function_name}\(.*?\):.*?return \"\"\"(.*?)\"\"\"",
        content,
        re.DOTALL,
    )

    if not match:
        raise ValueError(f"Query '{function_name}' not found in users_queries.sql")

    return match.group(1).strip()

@app.route('/')
def home():
    return '<h1>Flask REST API with PostgreSQL</h1>'

# CREATE
@app.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        password_hash = generate_password_hash(data['password_hash'])
        query = load_sql('create_new_user_query')
        cur.execute(query, (
            data['username'],
            data['email'],
            password_hash,
        ))
        return jsonify({"message": f"User '{data['username']}' created successfully"}), 201
    except psycopg2.errors.UniqueViolation:
        return jsonify({"error": "Username or email already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 400
      
# READ
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        query = load_sql('get_all_users_query')
        cur.execute(query)
        users = cur.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
      

# get user by email
@app.route('/user/<string:email>', methods=['GET'])
def get_user_by_email(email):
    try:
        query = load_sql('get_user_by_email_query')
        cur.execute(query, (email,))
        user = cur.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# get user by username
@app.route('/user/<string:username>', methods=['GET'])
def get_user_by_username(username):
    try:
        query = load_sql('get_user_by_username_query')
        cur.execute(query, (username,))
        user = cur.fetchone()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# UPDATE




# DELETE

# delete user
@app.route('/delete/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        query = load_sql('delete_user_query')
        cur.execute(query, (username,))
        if cur.rowcount > 0:
            return jsonify({"message": f"User '{username}' deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)