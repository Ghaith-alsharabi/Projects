# Forward Sports Basketball App

## Table of Contents
[[_TOC_]]

## Setup
```
Windows
$ git clone https://gitlab.com/BvdLind/forward-sports-basketball-dashboard
$ cd forward-sports-basketball-dashboard
$ python -m venv env
$ .\env\Scripts\activate
$ pip install -r requirements.txt
$ flask run
```

```
Mac & Linux
$ git clone https://gitlab.com/BvdLind/forward-sports-basketball-dashboard
$ cd fsBasketballApp
$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ flask run
```
### Config
The application uses [python-dotenv](https://pypi.org/project/python-dotenv/) to
look for a `.env` file at the root of the project directory for configuration purposes.
Inside the `.env` file environment variables are set.

One important environment variable to set is the `SECRET` environment variable,
because forms will not work without setting it.

Example of how to set an environment variable inside `.env`:
```
SECRET=secret
```

The names of environment variables the application looks for can be found inside
`config.py`.
