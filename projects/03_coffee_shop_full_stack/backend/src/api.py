import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
from .utilities.errorhandler import http_error_handler

app = Flask(__name__)

setup_db(app)
http_error_handler(app, jsonify)
CORS(app)

# ----------------------------------------------------------------------------
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# @DONE@
# ----------------------------------------------------------------------------

@app.route('/reset-db')
def reset_db():
    db_drop_and_create_all()
    return jsonify({
        'success': True,
        'message': 'db_drop_and_create_all @DONE!'
    }), 200

## ROUTES
@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': 'What up Dude.. do you want a coffee.!?'
    }), 200
# ----------------------------------------------------------------------------
# Read >> drinks list short
# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     GET /drinks
#         1. it should be a public endpoint
#         2. it should contain only the drink.short() data representation
#         3. returns status code 200 and json {"success": True, "drinks": drinks}
#            where drinks is the list of drinks or appropriate status code
#            indicating reason for failure
# @DONE
# ----------------------------------------------------------------------------

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks          = Drink.query.order_by(Drink.title).all()
    result          = [drink.short() for drink in drinks]
    total_results   = len(drinks)

    if total_results == 0:
        abort(404)

    return jsonify({
        'success':  True,
        'drinks':   result
    }), 200
# ----------------------------------------------------------------------------
# Read >> drinks list detail
# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     GET /drinks-detail
#       1. it should require the 'get:drinks-detail' permission
#       2. it should contain the drink.long() data representation
#       3. returns status code 200 and json {"success": True, "drinks": drinks}
#          where drinks is the list of drinks or appropriate status code
#          indicating reason for failure.
# ----------------------------------------------------------------------------

@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():

    drinks          = Drink.query.order_by(Drink.title).all()
    result          = [drink.long() for drink in drinks]
    total_results   = len(drinks)

    if total_results == 0:
        abort(404)

    return jsonify({
        'success':  True,
        'drinks':   result
    }), 200

# ----------------------------------------------------------------------------
# Create >> drink
# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     POST /drinks
#         1. it should create a new row in the drinks table
#         2. it should require the 'post:drinks' permission
#         3. it should contain the drink.long() data representation
#         4. returns status code 200 and json {"success": True, "drinks": drink}
#            where drink an array containing only the newly created drink
#            or appropriate status code indicating reason for failure
# @NOTES
    # recipe field data structure:
    # [{"color": "string", "name":"string", "parts":"number"}]
# ----------------------------------------------------------------------------

@app.route('/drinks', methods=['POST'])
def create_drink():

    title    = request.json.get('title', None)
    recipe   = json.dumps(request.json.get('recipe', None))

    if title is None or recipe is None:
        abort(400)

    drink = Drink(
        title   = title,
        recipe  = recipe
    )

    try:
        drink.insert()
    except:
        abort(422)

    return jsonify({
        'success':  True,
        'drink':    drink.long()
    }), 201

# ----------------------------------------------------------------------------
# Update >> drink
# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         1. it should respond with a 404 error if <id> is not found
#         2. it should update the corresponding row for <id>
#         3. it should require the 'patch:drinks' permission
#         4. it should contain the drink.long() data representation
#            returns status code 200 and json {"success": True, "drinks": drink}
#            where drink an array containing only the updated drink
#            or appropriate status code indicating reason for failure
# ----------------------------------------------------------------------------

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def update_drink(drink_id):

    drink = Drink.query.get_or_404(drink_id)

    title    = request.json.get('title', None)
    recipe   = json.dumps(request.json.get('recipe', None))

    if title is None or recipe is None:
        abort(400)

    drink.title = title
    drink.recipe = recipe

    try:
        drink.update()
    except:
        abort(400)

    return jsonify({
        'success':  True,
        'drink':    drink.long()
    }), 200

# ----------------------------------------------------------------------------
# Delete >> drink
# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         1. it should respond with a 404 error if <id> is not found
#         2. it should delete the corresponding row for <id>
#         3. it should require the 'delete:drinks' permission
#         4. returns status code 200 and json {"success": True, "delete": id}
#            where id is the id of the deleted record
#            or appropriate status code indicating reason for failure
# ----------------------------------------------------------------------------

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):

    drink = Drink.query.get_or_404(drink_id)

    try:
        drink.delete()
    except exc.SQLAlchemyError:
        abort(500)

    return jsonify({
        'success':  True,
        'delete':   drink_id
    }), 200

# ----------------------------------------------------------------------------
# Error Handling
# @TODO
#   1. implement error handlers using the @app.errorhandler(error) decorator
# @DONE
#   2. implement error handler for AuthError
# ----------------------------------------------------------------------------
