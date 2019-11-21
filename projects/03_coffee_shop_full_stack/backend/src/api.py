import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# ----------------------------------------------------------------------------
# @TODO uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
# @DONE@
# recipe field data structure:
# [{"color": "string", "name":"string", "parts":"number"}]
# ----------------------------------------------------------------------------

@app.route('/reset-db')
def reset_db():
    db_drop_and_create_all()
    return jsonify({
        'success': True,
        'message': 'db_drop_and_create_all @DONE!'
    })

## ROUTES
@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': 'What up Dude.. do you want a coffee.!?'
    })

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
    })

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
    })

# ----------------------------------------------------------------------------
# @TODO implement endpoint
#     POST /drinks
#         1. it should create a new row in the drinks table
#         2. it should require the 'post:drinks' permission
#         3. it should contain the drink.long() data representation
#         4. returns status code 200 and json {"success": True, "drinks": drink}
#            where drink an array containing only the newly created drink
#            or appropriate status code indicating reason for failure
# ----------------------------------------------------------------------------
# OK 200 | curl -X POST http://127.0.0.1:5000/drinks
# OK 201 | curl -X POST -H "Content-Type: application/json" -d '{"question":"Which is the result of 2+2 ?","answer":"4","difficulty":"100","category":"1"}' http://127.0.0.1:5000/drinks

@app.route('/drinks', methods=['POST'])
def create_drink():

    return jsonify({
        'success': True,
        'message': 'you POST in /drinks'
    })
# ----------------------------------------------------------------------------


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

# ----------------------------------------------------------------------------
# Error Handling
# @TODO
#   1. implement error handlers using the @app.errorhandler(error) decorator
#      each error handler should return (with approprate messages):
        # jsonify({
        #     "success": False,
        #     "error": 404,
        #     "message": "resource not found"
        # }), 404
# @DONE
#   2. implement error handler for AuthError
# ----------------------------------------------------------------------------

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422

#----------------------------------------------------------------------------#
