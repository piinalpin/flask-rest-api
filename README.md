# Simple REST Full API With Flask and SQLAlchemy (Python 3)

Tutorial for building Create, Read, Update and Delete using REST Full API with Flask and SQLAlchemy

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have installed Python 3 on your device

### Project structure
```
* flask-rest-api/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
```

### Step to create flask rest api

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment
```
pip install virtualenv
```
2. Create virtual environment and activate inside your flask-rest-api directory according the above structure
```
virtualenv venv
> On windows -> venv\Scripts\activate
> On linux -> . env/bin/activate
```
3. Install some third party librares on your virtual environment with pip
```
pip install flask sqlalchemy flask-sqlalchemy flask-migrate
```
4. Create `run.py` directory inside flask-project according the above structure
```python
from app import app
app.run(debug=True, host='127.0.0.1', port=5000)
```
5. Create `controller.py` according the abpove structure `flask-rest-api/app/module/`
```python
from flask import request, jsonify
from app import app

@app.route('/')
def index():
    return "<h1>Welcome to Flask Restful API</h1><p>Created By: Alvinditya Saputra</p>"
```
6. Create `__init__.py` inside app directory according the above structure `flask-rest-api/app/`
```python
from flask import Flask

app = Flask(__name__)

from app.module.controller import *
```
7. Run first this application to make sure can running with terminal or command promt
```
python run.py
```
9. Access `localhost:5000` according port that created in `run.py`

![Sample 1](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/1.PNG)

10. Configure the database with SQLAlchemy, you should create directory `db/` inside `app/` directory and modify `__init__.py` and it will be created `flask-api.db` inside `app` directory
```
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
```
```python
import os
from flask import Flask
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/flask-api.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

from app.module.controller import *
```
11. Define model to application and create database migration, you should create `models.py` file inside `module` directory according the above structure.
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa' #Must be defined the table name

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    nim = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, nim, name):
        self.nim = nim
        self.name = name

    def __repr__(self):
        return "<Name: {}, Nim: {}>".format(self.name, self.nim)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        students = Mahasiswa.query.all()
        result = []
        for student in students:
            obj = {
                'id': student.id,
                'nim': student.nim,
                'name': student.name
            }
            result.append(obj)
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit()
```
12. Run migration with flask-migrate, type in terminal as below
```
flask db init
flask db migrate
flask db upgrade
```
13. The structure of database should like as follows

Mahasiswa  |
------------- |
`id (Integer, PK, Autoincrement, NOT NULL)`  |
`name (String, NOT NULL)`  |
`nim (String, NOT NULL)`  |

14. Create constant class to define constant variable for example variable to HTTP status, you should create file `const.py` inside `app/module/` according the above structure
```python
class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400
```
15. The structure project will be look as follows
```
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- venv/
  |--- run.py
```
16. Import database from `models.py` and constant class `const.py` add this line `from .models import *` and `from .const import *` to the `controller.py`, it's mean import all class, function or variables from `models.py` and `const.py`
17. Create function to get data from Http Request GET to retrieve all data from database with endpoint `/mahasiswa`
```python
@app.route('/api/v1/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'mahasiswa': Mahasiswa.getAll()
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    return response
```
![Sample 2](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/2.PNG)

18. How to insert data to database with Http Request POST? Okay, lets do it with create function input data from request, add this code to function mahasiswa as `def mahasiswa()`
```python
    elif request.method == 'POST':
        nim = None if request.form['nim'] is "" else request.form['nim']
        name = None if request.form['name'] is "" else request.form['name']
        construct = {}
        try:
            mhs = Mahasiswa(nim=nim, name=name)
            mhs.save()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.CREATED
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
```
![Sample 3](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/3.PNG)

![Sample 4](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/4.PNG)

![Sample 5](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/5.PNG)

19. Then create function to filter or get data by id for which will use to PUT and DELETE request, that mean this function can update and delete data from database
```python
@app.route('/api/v1/mahasiswa/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mahasiswaId(id):
    mhs = Mahasiswa.query.filter_by(id=id).first()
    if request.method == 'GET':
        construct = {
            'error': [],
            'success': True,
            'mahasiswa': {
                'id': mhs.id,
                'nim': mhs.nim,
                'name': mhs.name
            }
        }
        response = jsonify(construct)
        response.status_code = HttpStatus.OK
    elif request.method == 'PUT':
        nim = None if request.form['nim'] is "" else request.form['nim']
        name = None if request.form['name'] is "" else request.form['name']
        construct = {}
        try:
            mhs.nim = nim
            mhs.name = name
            db.session.commit()
            construct['success'] = True
            construct['message'] = 'Data saved'
            response = jsonify(construct)
            response.status_code = HttpStatus.OK
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    elif request.method == 'DELETE':
        construct = {}
        try:
            mhs.delete()
            construct['success'] = True
            construct['message'] = 'Data has been delete.'
            response = jsonify(construct)
            response.status_code = HttpStatus.OK
        except Exception as e:
            construct['success'] = False
            construct['error'] = str(e)
            response = jsonify(construct)
            response.status_code = HttpStatus.BAD_REQUEST
    return response
```
![Sample 6](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/6.PNG)

![Sample 7](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/7.PNG)

![Sample 8](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/8.PNG)

![Sample 9](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/9.PNG)

![Sample 10](https://raw.githubusercontent.com/piinalpin/flask-rest-api/master/10.PNG)

### After change structure of flask project
```
* flask-rest-api/
  |--- app/
  |    |--- db/
  |    |    |--- flask-api.db
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- const.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- __init__.py
  |--- migrations/
  |--- venv/
  |--- run.py
```

### Want to demo online?
#### [Backend Flask REST API](https://flask-rest-api-maverick.herokuapp.com/)

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask Migrate](https://pypi.org/project/Flask-Migrate/) - The database migration
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used
* [SQL Alchemy](https://www.sqlalchemy.org/) - The database library
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Flask and SQL Alchemy connector

## Clone or Download

You can clone or download this project
```
> Clone : git clone https://github.com/piinalpin/flask-rest-api.git
```

## Authors

* **Alvinditya Saputra** - *Initial work* - [DSS Consulting](https://dssconsulting.id/) - [LinkedIn](https://linkedin.com/in/piinalpin) [Instagram](https://www.instagram.com/piinalpin) [Twitter](https://www.twitter.com/piinalpin)

