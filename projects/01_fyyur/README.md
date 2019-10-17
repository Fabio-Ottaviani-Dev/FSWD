# Fyyur

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── models.py  *** Your SQL Alchemy models
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

## Overall:
* Models are located in `models.py`.
* Controllers are located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


## Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user.
* `models.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

```sh
  $ cd ~
  $ sudo pip3 install Flask
```

To start and run the local development server,

**1. Initialize and activate a virtualenv:**
```sh
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env && source env/bin/activate
```

**2. Install the dependencies:**
```sh
  $ pip install -r requirements.txt
```

**3. db setup:**
```sh
  $ dropdb fyyur && createdb fyyur
  $ rm -r migrations/ # (if it's set)
  $ python models.py db init
  $ python models.py db migrate
  $ python models.py db upgrade

  $ psql fyyur
  $ \dt
              List of relations
   Schema |      Name       | Type  | Owner
  --------+-----------------+-------+-------
   public | alembic_version | table | XY
   public | artists         | table | XY
   public | shows           | table | XY
   public | venues          | table | XY
  (4 rows)

  \q
```

**4. Run the development server:**
```sh
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
```

**5. Navigate to Home page** [http://localhost:5000](http://localhost:5000)
