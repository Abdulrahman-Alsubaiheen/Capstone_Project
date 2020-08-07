# Full Stack Capstone Project (Casting Agency)

### Introduction
Casting-Agency is the final project in Udacity Nanodgree. The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

#### heroku Link

https://casting-agency-project-fsnd.herokuapp.com/

---

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

---

## API Reference

### Getting Started

- Authentication: This app has 3 Roles. Each has his own token which are provided in setup.sh file. 

### Roles

**Casting Assistant :**
- view:actors
- view:movies

**Casting Director :** 
- All permissions a Casting Assistant has
- create:actor
- delete:actor
- update:actor
- update:movie

**Executive Producer :**
- All permissions a Casting Director has
- add:movie
- delete:movie

---

### Error Handling
Errors are returned as JSON objects in the following format:

#### 400: Bad Request
#### 404: Resource Not Found
#### 405: Method not allowed
#### 422: Not Processable
#### 500: Internal Server Error

---

### Endpoints 

#### Actors

- #### GET '/actors'
    - General:
        - Fetch all Actor information
        - Request Arguments: None
        - Returns: JSON response containing all actors information, request status and the number of actors. 
        ```
        {
        "Actors": [
            {
            "age": 27,
            "gender": "male",
            "id": 1,
            "name": "ali"
            }
        ],
        "success": true,
        "total_Actors": 1
        }

        ```

- #### POST '/actors'
    - General
        - add new actor
        - Request Arguments: None
        - Request Body: Must include name(type str), gender(type str), age(type int)
        - Returns: Success value.
        ```
        {
            "success": true,
        }
        ```

- #### PATCH '/actors/int:actor_id'
    - General
        - edit the actor that has given
        - Request Arguments: actors_id
        - Request Body: name(type str), gender(type str) or age(type int)
        - Returns: Success value.
        ```
        {
            "success": true,
        }
        ```

- #### DELETE '/actors/int:actor_id'
    - General:
        - Deletes the actor that has given
        - Request Arguments: actors_id
        - Returns: Success value. 
        ```
        {
            "success": true,
        }
        ```


#### Movies

- #### GET '/movies'
    - General:
        - Fetch all Movies information
        - Request Arguments: None
        - Returns: JSON response containing all movies information, request status and the number of movies. 
        ```
        {
        "Movies": [
            {
            "id": 1,
            "release_date": "Mon, 13 Apr 2020 00:00:00 GMT",
            "title": "The End"
            }
        ],
        "success": true,
        "total_Movies": 1
        }
        ```

- #### POST '/movies'
    - General
        - add new movie
        - Request Arguments: None
        - Request Body: Must include title(type str), release_date(type datetime)
        - Returns: Success value.
        ```
        {
            "success": true,
        }
        ```

- #### PATCH '/movies/int:movie_id'
    - General
        - edit the movie that has given
        - Request Arguments: movies_id
        - Request Body: title(type str), release_date(type datetime
        - Returns: Success value.
        ```
        {
            "success": true,
        }
        ```

- #### DELETE '/movies/int:movie_id'
    - General:
        - Deletes the movie that has given
        - Request Arguments: movie_id
        - Returns: Success value. 
        ```
        {
            "success": true,
        }
        ```





## Testing
You can test the endpoint using Postman or Unittest.

### Unittest

python test_app.py
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```

#### Postman

the test endpoint in Heroku :-

Import Casting-Agency.postman_collection.json , then run the test
