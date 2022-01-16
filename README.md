# RECORD SHARE

Web app used for sharing, reviewing and discovery music records! 


# Features 

Using Psycopg2 and SQLAlchemy, the app uses a PostgreSQL database and runs on Flask. We use Marshmallow for serialization, Jinja2 for templating, Alembic for migrations, and Flask-Login for sessions.
A bucket on S3 is used for image upload and storage through boto3.

Record Share features a User model with login/logout functionality using session cookies, as well as a Records model.

Presently, tests are disabled. 

# Requirements

Python 3
pip
virtualenv
PostgreSQL

# Setup 

# CLONE REPO:

# CREATE VENV:
# /record_app/
virtualenv venv

# INSTALL Requirements:
# /record_app/
source venv/bin/activate

# CREATE DATABASE AND USER
psql postgres

>> CREATE DATABASE <db_name_here>;
>> CREATE USER <user_name_here> WITH PASSWORD '<password_here>';
>> GRANT ALL PRIVILEGES ON DATABASE <db_name_here> TO <user_name_here>;
>> \q

# /record_app/
pip install -r requirements.txt

# SET ENVIRONMENT VARIABLES.
 add a .env file to the /record_app/ directory

# CREATE/MIGRATE TABLES USING TERMINAL COMMANDS

Terminal commands for the app must be executed from the /record_app/record_app/ directory. Currently available commands are:

flask db-custom drop -> drops all tables

flask db-custom create -> (DEPRECATED) creates all tables

flask db init -> initializes the /migrations/ folder

flask db migrate -m "<migration note>" -> creates a new migration

flask db upgrade -> applies migrations (optional - specify a target migration)

flask db downgrade -> un-applies migrations (optional, specify a target migration)

# RUN APP

# /record_app/record_app/
flask run

