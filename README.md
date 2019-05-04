# FarmBot Translator

FarmBot Translator is a tool create by [Esieespace](https://esieespace.fr) to translate [Farmbot Web App](https://farmbot-translator.esieespace.fr)

You can use the version available at [https://farmbot-translator.esieespace.fr/](https://farmbot-translator.esieespace.fr/) or deploy your own.
## Configuration :
Create your own _var.env_ file from _var.env.dist_

## Installation :

- Clone the project

- Build docker images : `$ docker-compose build`

- Start containers : `$ docker-compose up -d`

- Create database `$ docker-compose exec web python manage.py migrate` 

- Create admin `$ docker-compose exec web python manage.py createsuperuser` 

- Go to [http://localhost:8000](http://localhost:8000) and login with the same e-mail