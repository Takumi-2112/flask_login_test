from flask import Flask, request, jsonify
import psycopg2
import os 
from werkzeug.security import generate_password_hash

app = Flask(__name__)

#setup pg db connection
conn = psycopg2.connect(
  dbname = os.getenv('FLASK_DB'),
  user= os.getenv('FLASK_DB_USER'),
  password= os.getenv('FLASK_DB_PASSWORD'),
  host= os.getenv('FLASK_DB_HOST'),
  port= os.getenv('FLASK_DB_PORT', '5432')
)

conn.autocommit = True
cur = conn.cursor()

# Helper to load SQL file functions
def load_sql(function_name):
 with open(os.path.join("db", "queries", "users_queries", f"{function_name}.sql"), "r") as file:
    return file.read()

@app.route('/')
def home():
    return '<h1>Flask REST API with PostgreSQL</h1>'

# CREATE
@app.route('/create', methods=['POST'])
def create_user():
  data = request.get_json()
  hashed_password = generate_password_hash(data['hashed_password'])
  query = load_sql('create_user_query')
  cur.execute(query, (
    data['name'],
    data['email'],
    hashed_password,
  ))
  return jsonify({"message": f"User '{data['name']}' created successfully"}), 201
    

# READ


# UPDATE


# DELETE