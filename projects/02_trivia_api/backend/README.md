# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip3 install -r backend/requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided.
From the backend folder in terminal run:
```bash

createdb trivia && psql trivia < trivia.psql

# test
createdb trivia_test && psql trivia_test < trivia.psql

psql trivia
\dt

#           List of relations
#  Schema |    Name    | Type  | Owner
# --------+------------+-------+-------
#  public | categories | table | Billy
#  public | questions  | table | Billy
# (2 rows)


```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
cd backend/
export FLASK_APP=flaskr && export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.


## Testing
To run the tests, run
```bash

dropdb trivia_test && createdb trivia_test
psql trivia_test < trivia.psql
```

Update the value of [id_question](https://github.com/Fabio-Ottaviani-Dev/FSWD/blob/f8949f0ce8ca894b5b80421f1ac1727807a66302/projects/02_trivia_api/backend/test_flaskr.py#L208) before run:

```bash

python3 test_flaskr.py

```

## Endpoints
### Create >> Question
POST /api/questions
Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
```bash
# Endpoint: POST /api/questions
# curl test
curl -X POST -H "Content-Type: application/json" -d '{"question":"Which is the result of 2+2 ?","answer":"4","difficulty":"100","category":"1"}' http://127.0.0.1:5000/api/questions
# Returns:
{
  "question": {
    "answer": "4",
    "category": 1,
    "difficulty": 100,
    "id": 33,
    "question": "Which is the result of 2+2 ?"
  },
  "success": true
}
```
### Read >> Questions
GET /api/questions
Endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
```bash
# Endpoint: GET /api/questions
# curl test
curl -X GET http://127.0.0.1:5000/api/questions?page=1
# Returns:
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category": "",
  "page": 1,
  "questions": [
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}

```
### Read >> Questions >> Search
POST /api/questions/search
Endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
```bash
# Endpoint: POST /api/questions/search
# curl test
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"lake"}' http://127.0.0.1:5000/api/questions/search
# Returns:
{
  "current_category": "",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
### # Read >> Questions >> by category
GET /api/categories/1/questions
Endpoint to get questions based on category.
```bash
# Endpoint: GET /api/categories/1/questions
# curl test
curl -X GET http://127.0.0.1:5000/api/categories/1/questions
# Returns:
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
### Read >> Questions >> to play
POST /api/quizzes
Endpoint to get questions to play the quiz, this endpoint should take category and previous question parameters and return a random questions within the given category.
```bash
# Endpoint: POST /api/quizzes
#Request Arguments: An object with the keys previous_questions and quiz_category

{
    "previous_questions": [5, 9, 12, 23],
    "quiz_category": {
        "type": "Sports",
        "id": 4
    }
}

# Returns:

{
	"success": true,
    "question": {
        "id": 2
        "question": "How many championships does the Lakers have?",
        "answer": "5",
        "difficulty": 1,
        "category": "4"
    }
}
```
### Delete >> Question >> by: id
DELETE /api/questions/2
Endpoint to DELETE question using a question ID
```bash
# Endpoint: DELETE /api/questions/2
# curl test
curl -X DELETE http://127.0.0.1:5000/api/questions/4
# Returns:
{
  "action": "delete",
  "id": 4,
  "success": true
}
```

### Read >> All Categories
GET /api/categories
Endpoint to handle GET requests, for all available categories.
```bash
# Endpoint: GET /api/categories
# curl test
curl -X GET http://127.0.0.1:5000/api/categories
# Returns:
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}

```
