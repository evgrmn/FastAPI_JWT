# FastAPI_JWT
A simple example of FastAPI user authentication using JWT. The functionality allows you to: create users; generate tokens; get user data; create user posts; view, update, delete user posts; put likes and dislikes on posts that do not concern the user.

## Installation
- download files 

I recommend to create venv

*In main folder:*
- python3 -m venv venv
> sudo apt install python3-venv *if 'venv' is not installed*
- source venv/bin/activate

*Install requirements:*
- pip install -r requirements.txt

*Start server:*
- uvicorn main:app --reload

*Start testing:*
http://localhost:8000/docs

![alt text](https://github.com/evgrmn/FastAPI_JWT/blob/main/pic.png?raw=true)

Works great, e.g., with Debian 11 and Python 3.9, Ubuntu 22.04 and Python 3.10

You can check the "database.db" file by typing in your terminal:

- sqlite3 database.db
> sudo apt install sqlite3 *if 'SQLite' is not installed*

Then try for example:

- select * from users;



