## Project setup

Note: There is a bash script `development`. When you see `python manage.py`,
you can type `./development` instead (sparing some typing). So you can do
something like `./development runserver`.


#### PostgreSQL

Make sure you have a PostgreSQL db with **version > 9.3** otherwise you won't be
able to use it with this project (we need JSON fields).

- Create the DB in PostgreSQL:

```
CREATE DATABASE <db_name>;
```

- You also want a user with permission to use this db.

> Later on...
> Take notes of the data needed to connect to your DB and put them in
> `legionella/omissis.py`, filling the correct variables in the db configuration.


#### create a virtualenv and install required packages

```
virtualenv .
. bin/activate
pip install -r requirements.txt
```


#### setup application settings (never commit omissis.py)

```
cd legionella
cp legionella/omissis.py.template legionella/omissis.py
```

> Now it's time to configure the DB in omissis.py. Fill the correct fields.


#### Setup PostgreSQL

This will create all the tables needed for your project.

```
python manage.py makemigrations
python manage.py migrate
```


#### Populate the PostgreSQL db

This command will create some dummy data to get you going with the work.

```
python manage.py populatedb
```

When bootstrapping the production application, the right command is:

```
python manage.py populateproddb
```

This one will create only 'real' data.


#### Create the admin user

```
python manage.py createsuperuser
```


#### start internal server

```
python manage.py runserver
```

The dev server listen to the port `8000`.


#### React - frontend build

Put the `build` folder inside the `frontend` folder.
Django will serve the react application.


## Excel Export

The request's route to export the data to an excel file is:

    /graphqlapp/download

It accepts both `GET` and `POST` requests.

Parameters:

- `startDate`
- `endDate`

both in the form `YYYY-MM-DD`. If they aren't both specified, we fall back as
usual: take the last two years.

Example:

    localhost:8000/graphqlapp/download?startDate=2018-03-01&endDate=2018-04-05

    localhost:8000/graphqlapp/download


## Releases

- version 0.5.0 in production on 20/04/2018


## Documentation

More info can be found at
https://sistemi.redturtle.it/kb/projects/legionella/index.html


---
