# horizon-travel
## Name
Horizon Travels

## Description
This project is built in [Flask](https://flask.palletsprojects.com/) using python 3.11.
You can also use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations for this project.

This project contains all routes relating to travel and travel related activities.


## MySQL Database
This project uses [MySQL](https://www.mysql.com/) database for storing data.

- You can download MySQL by this command:
```
sudo apt install mysql-server
```

- You can start MySQL server by this command:
```
sudo systemctl start mysql
```

- Run MySQL shell by this command:
```
sudo mysql
```

- Change root password by this command:
```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Password@123';
```

## Installation
- Configure [Pyenv](https://realpython.com/intro-to-pyenv/):
To configure pyenv you can follow this [tutorial](https://realpython.com/intro-to-pyenv/).

- Install mysql dependencies:
```
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

- Python Installation:
To run project, you must have python 3.11 installed on your system.
If python 3.11 is not installed pyenv will install it for you as you have already configured pyenv.

- Change Global Python Version:
```
pyenv global 3.11.0
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
