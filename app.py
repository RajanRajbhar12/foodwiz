from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__,
            template_folder=os.getcwd(),  # Use the current directory for templates
            static_folder=os.getcwd())  # Use the current directory for static files

# Custom route to serve static files
@app.route('/<filename>')
def serve_static_file(filename):
    return send_from_directory(os.getcwd(), filename)

# Other routes...

load_dotenv()
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients')

    if not ingredients:
        return jsonify({'error': 'Ingredients are required'}), 400

    # URL to find recipes by ingredients
    search_url = 'https://api.spoonacular.com/recipes/findByIngredients'
    search_params = {
        'ingredients': ingredients,
        'apiKey': SPOONACULAR_API_KEY,
        'number': 1  # Get 1 recipe to start
    }

    try:
        search_response = requests.get(search_url, params=search_params)
        print(f"Spoonacular response: {search_response.text}")  # Log the response

        if search_response.status_code != 200:
            return jsonify({'error': f"API error: {search_response.status_code} - {search_response.text}"}), 500

        recipes = search_response.json()

        if recipes:
            recipe_list = []
            for recipe in recipes:
                recipe_id = recipe['id']

                # Fetch detailed recipe information
                detail_url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
                detail_params = {'apiKey': SPOONACULAR_API_KEY}
                detail_response = requests.get(detail_url, params=detail_params)

                if detail_response.status_code != 200:
                    return jsonify({'error': f"API error: {detail_response.status_code} - {detail_response.text}"}), 500

                detailed_recipe = detail_response.json()

                # Construct the detailed recipe info
                recipe_list.append({
                    'title': detailed_recipe['title'],
                    'image': detailed_recipe['image'],
                    'ingredients': [
                        f"{ing['amount']} {ing['unit']} {ing['name']}" 
                        for ing in detailed_recipe['extendedIngredients']
                    ],
                    'instructions': detailed_recipe['instructions']
                })

            return jsonify({'recipes': recipe_list})
        else:
            return jsonify({'error': 'No recipes found for the given ingredients.'})

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return jsonify({'error': f"Request failed: {e}"}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
