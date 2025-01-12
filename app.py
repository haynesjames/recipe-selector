from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder='.')
CORS(app)

def get_random_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, image_url, cuisine, prep_time FROM recipes ORDER BY RANDOM() LIMIT 6")
    recipes = cursor.fetchall()
    conn.close()
    return [
        {
            'id': row[0],
            'name': row[1],
            'image_url': row[2],
            'cuisine': row[3],
            'prep_time': row[4],
        }
        for row in recipes
    ]

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/get-random-recipes', methods=['GET'])
def random_recipes():
    return jsonify(get_random_recipes())

if __name__ == '__main__':
    app.run(debug=True)