# Overview

There are altogether three services: 

* Service usage statistics,
* prediction according to features that user input and
* the relationship which user want to observe and the important elements that can affect popularity significantly.


# Setting up the backend
For backend you need run following commands in the root directory:


* Step 1: Install python packages (in the terminal)

```
pip3 install -r requirements.txt
```


* Step 2: Setup database

Run python interpreter:
`python3` or `python`

```python
# in python interpreter,
from backend import db, create_app
# if you want to drop existing database
db.drop_all()
# create database from model
db.create_all(app=create_app()
exit()  
```

* Step 3: Run the application (in the terminal)

```
export FLASK_APP=backend
export FLASK_ENV=development
flask run
```
