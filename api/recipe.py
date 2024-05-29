import json
from flask import Blueprint, request, jsonify
import requests
from flask_restful import Api, Resource

recipe_api = Blueprint('recipe_api', __name__,
                       url_prefix='/api/recipes')

api = Api(recipe_api)

class UserAPI:
    class _CRUD(Resource):
        def get(self, ingredients):  # Create method
            api_key = '84cfe45628de456c87a13a80b76f5bd8'  # Replace with your Spoonacular API key
            url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients=" + ingredients
            
            # Get allergens from query parameters
            allergens = request.args.get('allergens')
            if allergens:
                allergens = allergens.split(',')

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                if allergens:
                    # Filter out recipes containing any specified allergens in the name
                    for allergen in allergens:
                        data = [recipe for recipe in data if allergen.lower() not in recipe['title'].lower()]

                    # Further filter out recipes based on detailed ingredients if needed
                    filtered_data = []
                    for recipe in data:
                        recipe_id = recipe['id']
                        recipe_info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}"
                        recipe_info_response = requests.get(recipe_info_url)
                        
                        if recipe_info_response.status_code == 200:
                            recipe_info = recipe_info_response.json()
                            ingredient_names = [ingredient['name'] for ingredient in recipe_info['extendedIngredients']]
                            
                            # Check if any allergen is in the ingredients
                            if not any(allergen in ingredient_names for allergen in allergens):
                                filtered_data.append(recipe)
                        else:
                            return jsonify({"error": "Failed to fetch recipe details."}), recipe_info_response.status_code
                else:
                    filtered_data = data
                print(filtered_data)
                return jsonify(filtered_data)
            else:
                return jsonify({"error": "Failed to fetch recipes."}), response.status_code

    api.add_resource(_CRUD, '/getrecipes/<ingredients>')
