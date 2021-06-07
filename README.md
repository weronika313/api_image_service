# api_image_service
api for upload images via http requests and genereting url adresses to them

## Technologies used

* **[Python3](https://www.python.org/downloads/)** - A programming language
* **[DRF](https://www.django-rest-framework.org/)** - Django REST framework is a powerful and flexible toolkit for building Web APIs.
* **[Virtualenv](https://virtualenv.pypa.io/en/stable/)** - A tool to create isolated virtual environments
* **[Docker](https://docs.docker.com/)** – An open platform for developing, shipping, and running applications.
* **[Amazon S3](https://aws.amazon.com/s3/)** - Object storage built to store and retrieve any amount of data from anywhere


## Running

### Run locally

    $ docker-compose build
    $ docker-compose exec web python manage.py makemigrations --noinput
    $ docker-compose exec web python manage.py migrate --noinput
    $ docker-compose up -d
### load data
    $ docker-compose exec web python manage.py loaddata databasedump.json
    

## Usage

*  ### upload images 
*  ### generate expiring links
*  ### generate links to thumbnails

