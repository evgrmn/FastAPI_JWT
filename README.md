# FastAPI_JWT
A simple example of FastAPI user authentication using JWT. The functionality allows you to: create users; generate tokens; get user data; create user posts; view, update, delete user posts; put likes and dislikes on posts that do not concern the user.

## Installation
- download files 

I recommend to create venv

*In main folder:*
- python3 -m venv venv
- source venv/bin/activate

*Install requirements:*
- pip install -r requirements.txt

*Start server:*
- uvicorn main:app --reload

*Start testing:*
http://localhost:8000/docs

![alt text](https://github.com/evgrmn/FastAPI_JWT/pic.png?raw=true)
