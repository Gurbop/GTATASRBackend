import threading

# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
# database migrations
from model.users import initUsers
from model.players import initPlayers

# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition


# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    print(allowed_origin)
    print("-"*50)
    if allowed_origin in ['localhost:8086', 'http://127.0.0.1:8086', 'https://nighthawkcoders.github.io']:
        cors._origins = allowed_origin
    cors._origins = allowed_origin
# Create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Define a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()

# Register the custom command group with the Flask application
app.cli.add_command(custom_cli)
from flask import Flask, jsonify
from flask_cors import CORS
import requests
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjczNTI2N2FjLWYzNDQtNGY5Ni05OWFiLWEyYjRmMTU3MjYxOSIsImlhdCI6MTcxMjM1MzU1OSwic3ViIjoiZGV2ZWxvcGVyL2RkMDFmNzBiLTgzNGEtNzYyOC05ZGU3LWMxNWZjOWMxMGIxZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NC4yMzYuMTE2LjkzIiwiMjA5LjY2LjIwNS4xOTciXSwidHlwZSI6ImNsaWVudCJ9XX0.T1LIcKN-8ImN7VzqMKMu7m8pL9M3YyuLtOn2V_K9x8O4w7DQUSBKnZu9AFeR7n-OH5xkw2C-qb6dgnm5rG54AA"
API_BASE_URL = 'https://api.clashroyale.com/v1'
@app.route('/')
def home():
    return "Clash Royale Dashboard Backend"
@app.route('/challenges')
def fetch_challenges():
    url = f"https://api.clashroyale.com/v1/challenges"
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        challenges_list = []
        for item in data:
            challenges_list.extend(item.get('challenges', []))
        return jsonify(challenges_list)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
@app.route('/tournaments')
def get_tournaments():
    tournament_name = request.args.get('name', 'ydkv')  # Default value 'ydkv' if name parameter not provided
    url = f'https://api.clashroyale.com/v1/tournaments?name={tournament_name}'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return jsonify(response.json().get('items', []))  # Send back a list of items
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
@app.route('/leaderboard')
def get_leaderboard():
    season = request.args.get('season', '1')  # Default to season 1 if not specified
    url = f'https://api.clashroyale.com/v1/locations/global/seasons/{season}/rankings/players?limit=10'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return jsonify(response.json().get('items', []))  # Send back a list of items
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    print('here')
    app.run(debug=True, host="0.0.0.0", port="8086")

# server always runs on the address http://127.0.0.1:8086/
# http://127.0.0.1:8086/api/users/search
# http://127.0.0.1:8086/api/users/design
# http://127.0.0.1:8086/api/users/authenticate