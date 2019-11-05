import os

from flask import Flask, request, abort, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from  sqlalchemy.sql.expression import func, select

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

# ----------------------------------------------------------------------------
# @TODO: Set up CORS.
# Delete the sample route after completing the TODOs
# **DONE**
# ----------------------------------------------------------------------------

    CORS(app, resources={r"/api/*": {"origins": "*"}})

# ----------------------------------------------------------------------------
# @TODO: Use the after_request decorator to set:
# Allow '*' for origins
# Access-Control-Allow
# **DONE**

# CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        return response

# ----------------------------------------------------------------------------
# Create >> Question
# ----------------------------------------------------------------------------
# @TODO:
# Create an endpoint to POST a new question,
# which will require the question and answer text,
# category, and difficulty score.
#
# TEST: When you submit a question on the "Add" tab,
# the form will clear and the question will appear at the end of the last page
# of the questions list in the "List" tab.

# OK 201 | curl -X POST -H "Content-Type: application/json" -d '{"question":"Which is the result of 2+2 ?","answer":"4","difficulty":"100","category":"1"}' http://127.0.0.1:5000/api/questions
# OK 400 | curl -X POST -H "Content-Type: application/json" -d '{"question":"Which is the result of 2+2 ?","answer":"4","difficulty":"100"}' http://127.0.0.1:5000/api/questions
# **DONE**

    @app.route('/api/questions', methods=['POST'])
    def create_question():

        data = request.get_json()

        new_question    = data.get('question', None),
        answer          = data.get('answer', None),
        difficulty      = data.get('difficulty', None),
        category        = data.get('category', None)

        if new_question is None or answer is None or difficulty is None or category is None:
            abort(400)

        try:
            question = Question(
                question    = new_question,
                answer      = answer,
                difficulty  = difficulty,
                category    = category
            )

            question.insert()

            return jsonify({
                'success':  True,
                'question': question.format()
            }), 201 # 201 Created

        except:
            abort(422)

# ----------------------------------------------------------------------------
# Read >> Questions
# ----------------------------------------------------------------------------
# @TODO: Create an endpoint to handle GET requests for questions,
# including pagination (every 10 questions).
# This endpoint should return a list of questions,
# number of total questions, current category, categories.

# TEST: At this point, when you start the application
# you should see questions and categories generated,
# ten questions per page and pagination at the bottom of the screen for three pages.
# Clicking on the page numbers should update the questions.

# OK 200 | curl -X GET http://127.0.0.1:5000/api/questions?page=1
# OK 200 | curl -X GET http://127.0.0.1:5000/api/questions
# OK 404 | curl -X GET http://127.0.0.1:5000/api/questions?page=999

# **DONE**

    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        page        = request.args.get('page', 1, type=int)
        start       = (page - 1) * QUESTIONS_PER_PAGE
        end         = start + QUESTIONS_PER_PAGE

        questions   = Question.query.order_by(Question.category, Question.difficulty).all()
        total_questions = len(questions)

        if total_questions - (page * QUESTIONS_PER_PAGE) < 0:
            abort(404)

        try:
            questions_result    = [question.format() for question in questions]
            questions_set       = questions_result[start:end]

            categories          = Category.query.order_by(Category.id).all()
            categories_result   = [category.format() for category in categories]

            return jsonify({
                'success':          True,
                'questions':        questions_set,
                'total_questions':  total_questions,
                'current_category': '',
                'categories':       categories_result,
                'page':             page
            })
        except:
          abort(422)

# ----------------------------------------------------------------------------
# Read >> Questions >> Search
# ----------------------------------------------------------------------------
# @TODO:
# Create a POST endpoint to get questions based on a search term.
# It should return any questions for whom the search term
# is a substring of the question.
#
# TEST: Search by any phrase. The questions list will update to include
# only question that include that string within their question.
# Try using the word "title" to start.

# OK 200 | curl -X POST -H "Content-Type: application/json" -d '{"search":"which"}' http://127.0.0.1:5000/api/questions/search
# OK 400 | curl -X POST -H "Content-Type: application/json" -d '{"key":"which"}' http://127.0.0.1:5000/api/questions/search
# OK 404 | curl -X POST -H "Content-Type: application/json" -d '{"search":"sdsdsdsds"}' http://127.0.0.1:5000/api/questions/search
# **DONE**

    @app.route('/api/questions/search', methods=['POST'])
    def search_questions():

        data    = request.get_json()
        search  = data.get('search', None)

        if search is None:
            abort(400)

        questions = Question.query.filter(
            Question.question.ilike('%{}%'.format(search))
        ).all()

        total_questions = len(questions)

        if total_questions == 0:
            abort(404)
            #OR
            # return jsonify({
            #     'success':          False,
            #     'questions':        None,
            #     'total_questions':  total_questions,
            #     'current_category': ''
            # })

        try:
            questions_result    = [question.format() for question in questions]

            return jsonify({
                'success':          True,
                'questions':        questions_result,
                'total_questions':  total_questions,
                'current_category': ''
            })

        except:
          abort(422)

# ----------------------------------------------------------------------------
# Read >> Questions >> by category
# ----------------------------------------------------------------------------
# @TODO:
# Create a GET endpoint to get questions based on category.
#
# TEST: In the "List" tab / main screen, clicking on one of the
# categories in the left column will cause only questions of that
# category to be shown.

# 0K 200 | curl -X GET http://127.0.0.1:5000/api/categories/1/questions
# 0K 404 | curl -X GET http://127.0.0.1:5000/api/categories/999/questions

    @app.route('/api/categories/<int:id_category>/questions', methods=['GET'])
    def get_questions_by_category(id_category):

        questions = (Question.query.filter(
            Question.category == id_category
        ).all())

        total_questions = len(questions)

        if total_questions == 0:
            abort(404)

        questions_result = [question.format() for question in questions]

        try:
            return jsonify({
                'success':          True,
                'questions':        questions_result,
                'total_questions':  total_questions,
                'current_category': id_category
            })

        except:
            abort(422)

# ----------------------------------------------------------------------------
# Read >> Questions >> to play
# ----------------------------------------------------------------------------
# ideas:
# https://stackoverflow.com/questions/60805/getting-random-row-through-sqlalchemy
# https://pythonhosted.org/Flask-Session/

# @TODO:
# Create a POST endpoint to get questions to play the quiz.
# This endpoint should take category and previous question parameters
# and return a random questions within the given category,
# if provided, and that is not one of the previous questions.

# TEST: In the "Play" tab, after a user selects "All" or a category,
# one question at a time is displayed, the user is allowed to answer
# and shown whether they were correct or not.

    @app.route('/api/quizzes', methods=['POST'])
    def get_quiz_question():

        previous_questions  = request.json.get('previous_questions', None)
        quiz_category       = request.json.get('quiz_category', None)

        error = 422

        try:
            category = quiz_category.get('id')

            prevques = []
            for question in previous_questions:
                prevques.append(question)
        except:
            abort(400)
        try:
            if category == 0:
                next_question = Question.query.filter(~Question.id.in_(prevques)).order_by(func.random()).first()
            else:
                next_question = Question.query.filter(Question.category==category).filter(~Question.id.in_(prevques)).order_by(func.random()).first()

            if not next_question:
                error = 404
                abort(error)
            else:
                return jsonify({
                    'success': True,
                    'question': next_question.format()
                })
        except:
            abort(error)

# ----------------------------------------------------------------------------
# Delete >> Question >> by: id
# ----------------------------------------------------------------------------
# @TODO:
# Create an endpoint to DELETE question using a question ID.

# TEST: When you click the trash icon next to a question, the question will be removed.
# This removal will persist in the database and when you refresh the page.

# OK 200 | curl -X DELETE http://127.0.0.1:5000/api/questions/4
# OK 404 | curl -X DELETE http://127.0.0.1:5000/api/questions/999
# **DONE**

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'action': 'delete',
            'id': question.id
        })

# ----------------------------------------------------------------------------
# Read >> All Categories
# ----------------------------------------------------------------------------
# @TODO: Create an endpoint to handle GET requests, for all available categories.

# Test
# 01. OK 200 | curl -X GET http://127.0.0.1:5000/api/categories

    @app.route('/api/categories', methods=['GET'])
    def get_all_categories():
        categories          = Category.query.order_by(Category.id).all()
        response            = [category.format() for category in categories]
        total_categories    = len(categories)

        if total_categories == 0:
            abort(404)

        return jsonify({
            'success':          True,
            'categories':       response,
            'total_categories': total_categories
        })

# ----------------------------------------------------------------------------
# Error handler
# ----------------------------------------------------------------------------
    # @TODO: Create error handlers for all expected errors: including 404 and 422.
    # **DONE**

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

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

# ----------------------------------------------------------------------------

    return app
