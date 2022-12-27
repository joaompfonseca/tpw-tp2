# Formula 1 - Server (Django REST Framework)

## Description

This is a simple REST web service exposing an API for a Formula 1 database, written 
with the **Django REST Framework** using **Python3.8**. Its intended purpose is to
feed a web application written with the **Angular Framework** using **Node.js 18.12.1**.

Developed within the scope of the second practical work of Technologies and Web
Programming (2022/2023).

## Dependencies

This API was developed using **Python3.8** and requires the following
dependencies (see [Installation](#installation) section):

- django (3.1.2)
- djangorestframework (3.14.0)
- markdown (3.4.1)
- django-filter (21.1)
- django-cors-headers (3.11.0)

## Installation

- Run `pip3 install virtualenv` to install the module `virtualenv`.
- Run `virtualenv venv` in root to create a virtual environment.
- Run `source venv/bin/activate` in root to enter the virtual environment.
- Run `pip3 install -r requirements.txt` to install all project dependencies.

## Running the API

- Run `source venv/bin/activate` in root to enter the virtual environment.
- Run `python3 manage.py runserver` in root to start the API.
- The API should be running on [localhost:8000](http://localhost:8000/).
- Stop the API using `CTRL+C` in terminal.
- Run `deactivate` in root to exit the virtual environment.

## Public Deployment

- Click [here](https://joaompfonseca.pythonanywhere.com/) to access the API (Python Anywhere).
