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

### Step to create flask project

A step by step series of examples that tell you how to get a development env running

1. Install virtual environment
```
pip install virtualenv
```
2. Create virtual environment and activate inside your flask-project directory according the above structure
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
from flask import request
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

![Sample 1](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-1.PNG)
gambar1

10. Configure the database with SQLAlchemy, you should create directory `db/` inside `app/` directory and modify `__init__.py` and it will be created `flask-api.db` inside `app` directory
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
15. The structure of database should like as follows

Mahasiswa  |
------------- |
`id (Integer, PK, Autoincrement, NOT NULL)`  |
`name (String, NOT NULL)`  |
`nim (String, NOT NULL)`  |

16. Stop app if that is still running, press `CTRL+C` key to quit and type `python` to go to python terminal

![Sample 5](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-5.PNG)

17. Type command bellow to create database file `flaskcrud.db`
```
>>> from app.module.models import db
>>> db.create_all()
>>> exit()
```
18. The structure project will be look as follows
```
* flask-project/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- templates/ (html file)
  |    |--- __init__.py
  |    |--- flaskcrud.db
  |--- venv/
  |--- run.py
```
19. Import database from `models.py` add this line `from .models import db, Mahasiswa` to the `controller.py`, it's mean import from `models.py` for `db` variable and class `Mahasiswa`
20. Modify `controller.py` to create function to storing data of `Mahasiswa` then save to the database that is already made and retrieving data with `Mahasiswa.query.all()` it will be retrieving all data from database then made with `try` and `except` to handling an error
```python
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa(nim=nim, name=name)
            db.session.add(mhs)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    listMhs = Mahasiswa.query.all()
    print(listMhs)
    return render_template("home.html", data=enumerate(listMhs,1))
```
21. The statement of `data=enumerate(listMhs,1)` mean data will show from 1 and so on, not from the id

22. Then modify `home.html` file to show that data is already inputed on database from input form
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Crud</title>
</head>
<body>
<h3>Form Add Mahasiswa</h3>
<form action="/" method="POST">
    <table>
        <tr>
            <td>Nama Lengkap</td>
            <td>:</td>
            <td><input type="text" name="name"></td>
        </tr>
        <tr>
            <td>Nomor Induk Mahasiswa</td>
            <td>:</td>
            <td><input type="text" name="nim"></td>
        </tr>
        <tr>
            <td><button type="submit">Save</button></td>
        </tr>
    </table>
</form>

<h3>Data Mahasiswa</h3>
<table border="1">
    <tr>
        <th>No</th>
        <th>Nomor Induk Mahasiswa</th>
        <th>Nama</th>
    </tr>
    {% for no, x in data %}
        <tr>
            <td>{{ no }}</td>
            <td>{{ x.nim }}</td>
            <td>{{ x.name }}</td>
        </tr>
    {% endfor %}
</table>
</body>
</html>
```
![Sample 6](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-6.PNG)

23. Then modify `home.html` to add action button that will __UPDATE__ and __DELETE__ data from database using id from collection. On `href="form-update/{{ x.id }}"` it will be route to `/form-update/1` to GET parameters.
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Crud</title>
</head>
<body>
<h3>Form Add Mahasiswa</h3>
<form action="/" method="POST">
    <table>
        <tr>
            <td>Nama Lengkap</td>
            <td>:</td>
            <td><input type="text" name="name"></td>
        </tr>
        <tr>
            <td>Nomor Induk Mahasiswa</td>
            <td>:</td>
            <td><input type="text" name="nim"></td>
        </tr>
        <tr>
            <td><button type="submit">Save</button></td>
        </tr>
    </table>
</form>

<h3>Data Mahasiswa</h3>
<table border="1">
    <tr>
        <th>No</th>
        <th>Nomor Induk Mahasiswa</th>
        <th>Nama</th>
        <th>Action</th>
    </tr>
    {% for no, x in data %}
        <tr>
            <td>{{ no }}</td>
            <td>{{ x.nim }}</td>
            <td>{{ x.name }}</td>
            <td><a href="form-update/{{ x.id }}">Edit</a> | <a href="delete/{{ x.id }}">Delete</a></td>
        </tr>
    {% endfor %}
</table>
</body>
</html>
```
![Sample 7](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-7.PNG)

24. Then create `form-update.html` for the input form on update
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Crud</title>
</head>
<body>
<h3>Form Update Mahasiswa</h3>
<form action="/form-update" method="POST">
    <table>
        <tr>
            <td>Nama Lengkap</td>
            <td>:</td>
            <td><input type="text" name="name" value="{{ data.name }}"></td>
            <input type="hidden" name="id" value="{{ data.id }}">
        </tr>
        <tr>
            <td>Nomor Induk Mahasiswa</td>
            <td>:</td>
            <td><input type="text" name="nim" value="{{ data.nim }}"></td>
        </tr>
        <tr>
            <td><button type="submit">Update</button></td>
        </tr>
    </table>
</form>
</body>
</html>
```
![Sample 8](https://raw.githubusercontent.com/piinalpin/flask-crud/master/Image-8.PNG)

25. Then create function to __UPDATE__ data from the collections in `controller.py`, on __UPDATE__ you should create two function to load or render form input and update to database from method __POST__ on form input using `Mahasiswa.query.filter_by(id=id).first()` to find data filter by id and `db.session.commit()` to save the data
```python
@app.route('/form-update/<int:id>')
def updateForm(id):
    mhs = Mahasiswa.query.filter_by(id=id).first()
    return render_template("form-update.html", data=mhs)

@app.route('/form-update', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        nim = request.form['nim']
        try:
            mhs = Mahasiswa.query.filter_by(id=id).first()
            mhs.name = name
            mhs.nim = nim
            db.session.commit()
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/")
```
26. And modify import flask on top line change to `from flask import render_template, request, redirect`

27. Then create the __DELETE__ function to delete data from the collections in `controller.py` using filter by id and `db.session.delete(mhs)` function
```python
@app.route('/delete/<int:id>')
def delete(id):
    try:
        mhs = Mahasiswa.query.filter_by(id=id).first()
        db.session.delete(mhs)
        db.session.commit()
    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/")
```

### After change structure of flask project
```
* flask-project/
  |--- app/
  |    |--- module/
  |    |    |--- __init__.py
  |    |    |--- controller.py
  |    |    |--- models.py
  |    |--- templates/
  |    |    |--- form-update.html
  |    |    |--- home.html
  |    |--- __init__.py
  |    |--- flaskcrud.db
  |--- venv/
  |--- run.py
```

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Flask](http://flask.pocoo.org/) - The web framework used
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used
* [SQL Alchemy](https://www.sqlalchemy.org/) - The database library
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) - Flask and SQL Alchemy connector

## Clone or Download

You can clone or download this project
```
> Clone : git clone https://github.com/piinalpin/flask-crud.git
```

## Authors

* **Alvinditya Saputra** - *Initial work* - [DSS Consulting](https://dssconsulting.id/) - [LinkedIn](https://linkedin.com/in/piinalpin) [Instagram](https://www.instagram.com/piinalpin) [Twitter](https://www.twitter.com/piinalpin)

