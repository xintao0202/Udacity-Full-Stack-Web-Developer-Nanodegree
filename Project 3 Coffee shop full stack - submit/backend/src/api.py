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

'''
@uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES

'''
@implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=['GET'])
def get_drinks():
    try:
        body = Drink.query.all()
        drinks = [drink.short() for drink in body]
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200
    except Exception:
        abort(500)


'''
@implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(token):
    try:
        body = Drink.query.all()
        drinks = [drink.long() for drink in body]

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except Exception:
        abort(500)


'''
@implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drinks(payload):
    body = request.get_json()
    if not body:
        abort(404)
    new_recipe = body.get('recipe', None)
    new_recipe = json.dumps(new_recipe)
    new_title = body.get("title", None)

    try:
        drink = Drink(recipe=new_recipe, title=new_title)
        drink.insert()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except Exception:
        abort(422)


'''
@implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drinks(*args, **kwargs):
    body = request.get_json()
    drink = Drink.query.filter_by(id=kwargs.get("id")).one_or_none()
    if not drink:
        abort(404)
    new_recipe = body.get("recipe")
    new_title = body.get("title")

    try:
        if isinstance(drink.recipe, list):
            drink.recipe = json.dumps(new_recipe)
        drink.title = new_title
        drink.update()
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except Exception:
        abort(404)


'''
@implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<drink_id>", methods=['DELETE'])
@requires_auth("delete:drinks")
def delete_drinks(payload, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.delete()
        result = {
            "success": True,
            "drinks": drink_id
        }
        return jsonify(result)
    except Exception:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
            }), 422


'''
@implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@implement error handler for 404
error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


'''
@implement error handler for AuthError
error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


# Other error handlers
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'An error has occured, please try again'
    }), 500
