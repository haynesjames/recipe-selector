from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='static')  # Use 'static' for local files
CORS(app)

# Function to fetch random recipes from the database
def get_random_recipes():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, image_url, cuisine, prep_time, recipe_url 
        FROM recipes 
        ORDER BY RANDOM() 
        LIMIT 6
    """)
    recipes = cursor.fetchall()
    conn.close()
    return [
        {
            'id': row[0],
            'name': row[1],
            # Build the correct image URL
            'image_url': f'static/{row[2]}' if row[2] else 'static/placeholder.jpg',
            'cuisine': row[3],
            'prep_time': row[4],
            'recipe_url': row[5]
        }
        for row in recipes
    ]

# Route to serve the main index.html page
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Route to fetch random recipes
@app.route('/get-random-recipes', methods=['GET'])
def random_recipes():
    return jsonify(get_random_recipes())

# Route to fetch a specific recipe by ID
@app.route('/get-recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, image_url, cuisine, prep_time, ingredients, instructions
        FROM recipes
        WHERE id = ?
    """, (recipe_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            'id': row[0],
            'name': row[1],
            'image_url': row[2] if row[2] and os.path.exists(os.path.join(app.static_folder, row[2])) 
                          else 'static/placeholder.jpg',
            'cuisine': row[3],
            'prep_time': row[4],
            'ingredients': row[5],
            'instructions': row[6],
        })
    else:
        return jsonify({'error': 'Recipe not found'}), 404

# Serve static files such as images
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)