import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from datamodel import datamodel
from auth_middleware import token_required

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            print("I MILLY ROCK")
            print("here1111111")
            body = request.get_json()
            print("here1111112")
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            print("here1111111")
            password = body.get('password')
            dob = body.get('dob')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(name=name, 
                      uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required()
        def get(self, _): # Read Method, the _ indicates current_user is not used
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
   
        @token_required("Admin")
        def delete(self, _): # Delete Method
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 404
            json = user.read()
            user.delete() 
            # 204 is the status code for delete with no json response
            return f"Deleted user: {json}", 204 # use 200 to test with Postman
        
    class Prediction(Resource):
        def post(self):
            # maintry:
                body = request.get_json()
                gpa = float(body.get('gpa'))
                SAT = int(body.get('SAT'))
                Extracurricular_Activities = int(body.get('Extracurricular_Activities'))
                Model = datamodel()
                prediction_result = Model.predict(gpa, SAT, Extracurricular_Activities)
                if prediction_result == "Rejected": # switching data
                    return jsonify("Accepted")
                elif prediction_result == "Accepted":
                    return jsonify("Rejected")
                return jsonify(prediction_result)
            # except Exception as e:
                # print("Prediction error:", str(e))  # Log the error
                # return {
                #     "message": "Something went wrong during prediction!",
                #     "error": str(e),
                #     "data": None
                # }, 500      

    class Images(Resource):
        @token_required()
        def post(self, _):
            print("here","millyrock"*50)
            token = request.cookies.get("jwt")
            cur_user = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid'] # current user
            body=request.get_json()
            base64=body.get("Image")
            print(base64[:10])
            users = User.query.all()
            for user in users:
                print(user.uid,cur_user)
                if user.uid == cur_user:
                    print("finding")
                    user.updatepfp(base64)
            return jsonify("works")
        
        @token_required()
        def get(self, _):
            print('here')
            print("here")
            print("ANKITBADBOY"*20)
            token = request.cookies.get("jwt")
            cur_user = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid'] # current user
            users = User.query.all()
            for user in users:
                if user.uid == cur_user:
                    return jsonify(user.getprofile())
                
            
    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 401
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 401
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

    class AddFriend(Resource):
        @token_required()
        def post(self, _):
            print("in here")
            try:
                # Get the friend's user ID from the request body
                data = request.get_json()
                friend_uid = data.get('friend_uid')

                # Find the current user based on the JWT token
                token = request.cookies.get("jwt")
                current_user_uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid']
                current_user = User.query.filter_by(_uid=current_user_uid).first()

                # Find the friend user based on the user ID
                friend = User.query.filter_by(_uid=friend_uid).first()

                # Check if the friend exists
                if not friend:
                    return {'message': 'Friend not found'}, 404

                # Add the friend to the current user's friend list
                print("Adding friend", friend.uid)
                current_user.addfriend(friend.uid)

                return {'message': 'Friend added successfully'}, 200

            except Exception as e:
                return {'message': str(e)}, 500        
        @token_required()
        def put(self, _):
            data = request.get_json()
            personuid = data.get('useruid')
            users = User.query.all()    # read/extract all users from database
            friends={}
            for user in users:
                friends[user.uid]=[]
            for user in users:
                friends[user.uid]=user.getfriends()
            token = request.cookies.get("jwt")
            current_user_uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid']
            visited = set()
            level = [current_user_uid]
            result = []
            levels = []
            node_levels = {current_user_uid: 0}  # Dictionary to store levels of each node
            
            current_level = 0

            while level:
                next_level = []
                levels.append(level.copy())

                while level:
                    current_node = level.pop(0)

                    if current_node not in visited:
                        visited.add(current_node)
                        result.append(current_node)

                        for neighbor in friends[current_node]:
                            if neighbor not in visited and neighbor not in next_level:
                                next_level.append(neighbor)
                                node_levels[neighbor] = current_level + 1  # Set level of neighbor

                level = next_level
                current_level += 1
            maxvalues=max(node_levels.values())+1
            for user in users:
                if(user.uid not in node_levels.keys()):
                    node_levels[user.uid]=maxvalues
            return jsonify({'level':str(node_levels[personuid])})
            
        @token_required()
        def get(self,_):
            users = User.query.all()    # read/extract all users from database
            friends={}
            for user in users:
                friends[user.uid]=[]
            for user in users:
                friends[user.uid]=user.getfriends()
            token = request.cookies.get("jwt")
            current_user_uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid']
            visited = set()
            level = [current_user_uid]
            result = []
            levels = []
            node_levels = {current_user_uid: 0}  # Dictionary to store levels of each node
            
            current_level = 0

            while level:
                next_level = []
                levels.append(level.copy())

                while level:
                    current_node = level.pop(0)

                    if current_node not in visited:
                        visited.add(current_node)
                        result.append(current_node)

                        for neighbor in friends[current_node]:
                            if neighbor not in visited and neighbor not in next_level:
                                next_level.append(neighbor)
                                node_levels[neighbor] = current_level + 1  # Set level of neighbor

                level = next_level
                current_level += 1
            maxvalues=max(node_levels.values())+1
            for user in users:
                if(user.uid not in node_levels.keys()):
                    node_levels[user.uid]=maxvalues
            json_ready=[]
            for user in users:
                value=user.read()
                appender=list(value.values())
                appender2=appender.copy()
                appender2.append(node_levels[user.uid])
                json_ready.append(appender2)
                
            # quicksort
            def partition(arr, low, high, column_index):
                pivot = arr[high][column_index]
                i = low - 1
                for j in range(low, high):
                    if arr[j][column_index] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                return i + 1
            def quicksort(arr, low, high, column_index):
                if low < high:
                    pi = partition(arr, low, high, column_index) 
                    quicksort(arr, low, pi - 1, column_index) 
                    quicksort(arr, pi + 1, high, column_index) 
            quicksort(json_ready,0,len(json_ready)-1,6)
            
            
            return jsonify(json_ready)
            
    class social(Resource):
        @token_required()
        def get(self,_): #get friend list
            token = request.cookies.get("jwt")
            current_user_uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['_uid']
            users=User.query.all()
            for user in users:
                if(user.uid==current_user_uid):
                    return jsonify(user.getfriends())
                
        
        
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(Images,'/images')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(Prediction, '/Prediction')
    api.add_resource(AddFriend, '/add-friend')
    api.add_resource(social,'/social')
