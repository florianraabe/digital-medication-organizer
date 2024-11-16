# MedApp - A digital medication organizer



## Setup

The first thing to do is to clone the repository:

```console
$ git clone https://github.com/florianraabe/digital-medication-organizer.git
$ cd digital-medication-organizer
```

Create a virtual environment to install dependencies in and activate it:

```console
$ python -m venv venv
$ source venv/bin/activate
```

Then install the dependencies:

```console
(venv) $ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies, setup the database:

```console
(venv) $ python manage.py makemigrations
(venv) $ python manage.py migrate
```

And start the application server:

```console
(venv) $ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.