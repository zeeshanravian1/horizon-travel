# horizon-travel
## Name
Horizon Travels

## Description
This project is built in [Flask](https://flask.palletsprojects.com/) using python 3.11.
You can also use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations for this project.

This project contains all routes relating to travel and travel related activities.

## Installation
- Python Installation:
To install project dependencies you must have python 3.11 installed on your system.
If python 3.11 is not installed you can download it from [python website](https://www.python.org/downloads/) or you can configure your system to handle multiple python versions using [pyenv](https://realpython.com/intro-to-pyenv/).

Verify your python installation by typing this command in your terminal:
```
python --version
```

- Pipenv Installation:
After that, you need to install pipenv to handle virtual environments, you can install it by typing this command in your terminal:
```
pip install pipenv or
pip3 install pipenv
```

Adding pipenv to path
```
echo 'export PATH="/home/<user>/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Verify your pipenv installation:
```
pipenv
```

- Creating Virtual Environment
Go to project directory and type following command in terminal.
```
pipenv sync
```

This will create a virtual environment for your project along with dependencies.

- Activate Virtual Environment
To active virtual environment type following command in terminal.
```
pipenv shell
```

You can verify your environment dependencies by running:
```
pip list
```

## Configure [Alembic](https://alembic.sqlalchemy.org/en/latest/) for Database Migrations.
- Type following command to initialize migrations
```
alembic init migrations
```
We have already added migrations folder to project, you can skip above step.
- Edit env.py in migrations folder to set path for your database:
We have already added migrations folder to project, you can skip above step.

- Your first migrations
```
alembic revision --autogenerate -m "<Migration Name>"
```

- Apply Migrations
```
alembic upgrade heads
```
