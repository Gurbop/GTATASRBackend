from flask import Flask, request, jsonify
import json
import sqlite3
from flask_cors import CORS
# Intializes app as a flask application
app = Flask(__name__)
# CORS policies
cors = CORS(app, resources={r"/average/*": {"origins": "*"}})
cors = CORS(app, resources={r"/getrev/*": {"origins": "*"}})
cors = CORS(app, resources={r"/*": {"origins": "*"}})
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('reviews.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn
@app.route('/reviews/<name>', methods =['GET'])
def reviews_by_name(name):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM reviews WHERE name=?", (name,))
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews:
            return jsonify(reviews)
        else:
            return "No reviews found for this name!!", 404
@app.route('/getrev', methods=['GET'])
def getreviews():
    if request.method == "GET":
        conn = db_connection()
        cursor = conn.cursor
        rate = None
        cursor = conn.execute("SELECT * FROM reviews")
        reviews = [
            dict(id=row[0], name=row[1], review=row[2], rate=row[3])
            for row in cursor.fetchall()
        ]
        if reviews is not None:
            return jsonify(reviews)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)






