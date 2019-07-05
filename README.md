# Flask REST Api with Python 3

<h3 align=center>
=> tuto slides: http://bit.ly/flask-rest-api-tuto <=
</h3>

## Kezako
This is a little Flask App showing [my] good practices for creating REST apis with Flask.

It presents two main methods:

* using basic Flask (and Flask-wtf),
* using Flask-RESTful

More importantly, it shows how to:

* structure an app
* test an app
* use setuptools to package an app

## Setup

```bash
git clone git@github.com:derlin/flask-rest-api-tuto.git
cd flask-rest-api-tuto
python setup.py install
```

## Run

From the terminal:
```bash
python -m llapp run
```

Using docker (will be available on http://localhost:80):
```bash
docker build --rm -t llapp .
docker run --rm -d --name llapp -p 80:80 llapp
```

Using gunicorn:
```bash
pip install gunicorn
gunicorn "llapp:create_app()"
```