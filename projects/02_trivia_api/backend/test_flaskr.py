import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

# ----------------------------------------------------------------------------
# Create >> Question
# ----------------------------------------------------------------------------
    # successful operation
    def test_create_question(self):
        new_question = {
            'question':'Which is the result of 2+2 ?',
            'answer':'4',
            'difficulty':'100',
            'category':'1'
        }

        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)

        question = (Question.query.filter(Question.question == new_question['question']).first())

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        (self.assertEqual(data['question']['question'],new_question['question']))

    # expected error / s
    def test_create_question_400(self):
        new_question = {
            'question':'Which is the result of 3+5 ?',
            'answer':'8',
            'difficulty':'100',
        }

        res = self.client().post('/api/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

# ----------------------------------------------------------------------------
# Read >> Questions
# ----------------------------------------------------------------------------
    # successful operation
    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    # expected error / s
    def test_get_questions_404(self):
        res = self.client().get('/api/questions?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# ----------------------------------------------------------------------------
# Read >> Questions >> Search
# ----------------------------------------------------------------------------

# OK 200 | curl -X POST -H "Content-Type: application/json" -d '{"search":"which"}' http://127.0.0.1:5000/api/questions/search
# OK 400 | curl -X POST -H "Content-Type: application/json" -d '{"key":"which"}' http://127.0.0.1:5000/api/questions/search

    # successful operation
    def test_search_question(self):
        res = self.client().post('/api/questions/search', json={"search":"Who discovered penicillin"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)

    # expected error / s
    def test_search_question_400(self):
        res = self.client().post('/api/questions/search', json={"key":"Who discovered penicillin"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

# ----------------------------------------------------------------------------
# Read >> Questions >> by category
# ----------------------------------------------------------------------------
    # successful operation
    def test_get_questions_by_category(self):

        id_category = 1

        res = self.client().get('/api/categories/{}/questions'.format(id_category))
        data = json.loads(res.data)

        questions = (Question.query.filter(
            Question.category == id_category
        ).all())

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])


    # expected error / s
    def test_get_questions_by_category_404(self):
        id_category = 999

        res = self.client().get('/api/categories/{}/questions'.format(id_category))
        data = json.loads(res.data)

        questions = (Question.query.filter(
            Question.category == id_category
        ).all())

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# ----------------------------------------------------------------------------
# Read >> Questions >> to play
# ----------------------------------------------------------------------------
#  id |     type
# ----+---------------
#   1 | Science
#   2 | Art
#   3 | Geography
#   4 | History
#   5 | Entertainment
#   6 | Sports

    # successful operation
    def test_next_quiz_question(self):

        quiz_1 = {
            'previous_questions':[13,14],
            'quiz_category':{
                'type': 'Geography',
                'id': 3
            }
        }

        res = self.client().post('/api/quizzes', json=quiz_1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    # expected error / s
    def test_next_quiz_question_404(self):

        quiz_2 = {
            'previous_questions':[10,11],
            'quiz_category':{
                'type': 'Sports',
                'id': 6
            }
        }

        res = self.client().post('/api/quizzes', json=quiz_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# ----------------------------------------------------------------------------
# Delete >> Question >> by: id
# ----------------------------------------------------------------------------
    # successful operation
    def test_delete_question(self):
        id_question = 46

        res = self.client().delete('/api/questions/{}'.format(id_question))
        data = json.loads(res.data)
        question = Question.query.get(id_question)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    # expected error / s
    def test_delete_question_404(self):
        id_question = 999

        res = self.client().delete('/api/questions/{}'.format(id_question))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

# ----------------------------------------------------------------------------
# Read >> All Categories
# ----------------------------------------------------------------------------
    # successful operation
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    # expected error / s
    def test_get_categories405(self):
        res = self.client().post('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

# ----------------------------------------------------------------------------


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
