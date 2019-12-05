# Deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild

The Flask app that will be used for this project consists of a simple API with three endpoints:

- `GET '/'`: This is a simple health check, which returns the response 'Healthy'.
- `POST '/auth'`: This takes a email and password as json arguments and returns a JWT based on a custom secret.
- `GET '/contents'`: This requires a valid JWT, and returns the un-encrpyted contents of that token.

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.

# Project Overview

1. Local Test
2. Write a Dockerfile for a simple Flask API
3. Build and test the container locally
4. Create an EKS cluster
5. Store a secret using parameter store
5. Create a CodePipeline pipeline triggered by GitHub checkins
6. Create a CodeBuild stage which will build, test, and deploy your code

# Local Test

```bash
#------------------------------------------------------------------------------
# Setup
#------------------------------------------------------------------------------

# virtualenv: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
deactivate

# start | Doc CLI: https://flask.palletsprojects.com/en/1.1.x/cli/
source env/bin/activate &&
export JWT_SECRET='myjwtsecret' &&
export LOG_LEVEL=DEBUG &&
export FLASK_APP=main.py &&
export FLASK_ENV=development &&  
export FLASK_RUN_PORT=8080 &&
flask run --reload

#------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------
curl -X GET http://0.0.0.0:8080
# "Healthy"

#/auth endpoint
export TOKEN=`curl -d '{"email":"test@mail.com","password":"asso123"}' -H "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100   224  100   178  100    46   4818   1245 --:--:-- --:--:-- --:--:--  4810

 echo $TOKEN
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzY3MTAzNTIsIm5iZiI6MTU3NTUwMDc1MiwiZW1haWwiOiJ0ZXN0QG1haWwuY29tIn0.xqT8qMZVGwLfDiO5354I1sIOZTV4XET7LaIXiqZXjog

# /contents endpoint
curl --request GET 'http://127.0.0.1:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .

#   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
#                                  Dload  Upload   Total   Spent    Left  Speed
# 100    75  100    75    0     0   2793      0 --:--:-- --:--:-- --:--:--  2884
# {
#   "email": "test@mail.com",
#   "exp": 1576709954,
#   "nbf": 1575500354
# }

```

# Dependencies

- Docker Engine
    - Installation instructions for all OSes can be found [here](https://docs.docker.com/install/).
    - For Mac users, if you have no previous Docker Toolbox installation, you can install Docker Desktop for Mac. If you already have a Docker Toolbox installation, please read [this](https://docs.docker.com/docker-for-mac/docker-toolbox/) before installing.
 - AWS Account
     - You can create an AWS account by signing up [here](https://aws.amazon.com/#).
