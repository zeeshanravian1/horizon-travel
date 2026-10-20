# Horizon Travels

A [Flask](https://flask.palletsprojects.com/) web application that provides the routes for travel and travel-related activities. It is built with Python 3.11, stores its data in [MySQL](https://www.mysql.com/), and manages database migrations with [Alembic](https://alembic.sqlalchemy.org/en/latest/).

## Table of Contents

- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Database Setup](#database-setup)
- [Installation](#installation)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)

## Tech Stack

| Component       | Technology                                                   |
| --------------- | ------------------------------------------------------------ |
| Language        | Python 3.11                                                  |
| Web framework   | [Flask](https://flask.palletsprojects.com/)                  |
| Database        | [MySQL](https://www.mysql.com/)                              |
| Migrations      | [Alembic](https://alembic.sqlalchemy.org/en/latest/)         |
| Python versions | [pyenv](https://realpython.com/intro-to-pyenv/)              |
| Environment     | [Pipenv](https://pipenv.pypa.io/)                            |

## Prerequisites

- MySQL server
- [pyenv](https://realpython.com/intro-to-pyenv/), configured as described in [this tutorial](https://realpython.com/intro-to-pyenv/)
- Python 3.11 (pyenv will install it if it is missing)
- Pipenv
- MySQL client development libraries (see [Installation](#installation))

## Database Setup

1. Install MySQL (Ubuntu/Debian):

   ```bash
   sudo apt install mysql-server
   ```

2. Start the MySQL server:

   ```bash
   sudo systemctl start mysql
   ```

3. Open the MySQL shell:

   ```bash
   sudo mysql
   ```

4. Set the root password:

   ```sql
   ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Password@123';
   ```

   > **Note:** `Password@123` is an example for local development only. Use a strong password in any shared or production environment.

5. Create the application database:

   ```sql
   CREATE DATABASE IF NOT EXISTS horizontravels_database;
   ```

## Installation

### 1. Install MySQL client dependencies

**Ubuntu/Debian:**

```bash
sudo apt-get install pkg-config python3-dev default-libmysqlclient-dev build-essential
```

**macOS:**

```bash
brew install pkg-config mysql-client
```

On macOS, also add `mysql-client` to your `pkg-config` path by adding it to your shell configuration file (e.g. `~/.zshrc` or `~/.bashrc`):

```bash
echo 'export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"' >> ~/.zshrc
```

### 2. Set the Python version

With pyenv configured, set Python 3.11 as the global version:

```bash
pyenv global 3.11.0
```

### 3. Install Pipenv

Pipenv manages the project's virtual environment:

```bash
pip install pipenv
# or
pip3 install pipenv
```

Add Pipenv to your `PATH` (replace `<user>` with your username):

```bash
echo 'export PATH="/home/<user>/.local/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

Verify the installation:

```bash
pipenv
```

### 4. Create the virtual environment

From the project root, create the virtual environment and install all dependencies:

```bash
pipenv sync
```

### 5. Activate the virtual environment

```bash
pipenv shell
```

Optionally, confirm the installed dependencies:

```bash
pip list
```

## Database Migrations

The `migrations` folder is already included in this project, so you do **not** need to run `alembic init` or edit `migrations/env.py` to set the database path. For reference, a new Alembic setup is initialized with:

```bash
alembic init migrations
```

Generate a migration after changing the models:

```bash
alembic revision --autogenerate -m "<Migration Name>"
```

Apply all pending migrations:

```bash
alembic upgrade heads
```

## Running the Application

Start the development server with debug mode enabled:

```bash
flask --app main.py --debug run
```
