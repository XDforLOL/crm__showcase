## A-digit CRM and Ecommerce web application App
This is  an independent project created to showcase CRM and Ecommerce 

## Description

#### Welcome to my (Django-bootstrap 4) CRM and Ecommerce web application
stacked within a docker container running with a Psql Database, Hosted on a raspberry pi.
In this App the business can create orders, search the orders that were created, follow customer orders and update them as needed,
While the customer has the options; to place orders with a functional shopping cart, get updated at what stage the order is and look at order history.


## Features
- Admin has CRM features
- User can browse the product catalog and add to Shopping cart 
- Users also can checkout and place Orders 
- Admin can monitor edit user orders if needed 

## Technologies Used
    - Python 3.8
    - Django framework
    - Docker container
    - JavaScript
    - PostgreSQL
    - Raspberry PI server
    - HTML, CSS and Bootstrap
 

### Prerequisite
The project requires a prerequisite understanding of the following:
- Django Framework
- Python
- PostgreSQL
- Docker containers
- Raspbian

## Setup and installation

#### Clone the Repo

####  Install dependancies
run pip install in your venv `pip3 install -r requirements.txt`

####  Create the Database
    - psql
    - CREATE DATABASE retaildb;

####  .env file

Create .env file and paste paste the following filling where appropriate:

    SECRET_KEY = '<Secret_key>'
    DBNAME = 'retaildb'
    USER = '<Username>'
    PASSWORD = '<password>'
    DEBUG = True

#### Run initial Migration
    python 3.8 manage.py makemigrations retaildb
    python 3.8 manage.py migrate

#### Run the app
    python 3.8 manage.py runserver
    Open terminal on localhost:8000

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
