from flask import Flask, request, jsonify
import psycopg2
import os 

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

# Helper to load SQL files
def load_sql(filename):
    with open(os.path.join("db", "queries", filename), "r") as file:
        return file.read()

@app.route('/')
def home():
    return '<h1>Flask REST API with PostgreSQL</h1>'

# CREATE


# READ


# UPDATE


# DELETE