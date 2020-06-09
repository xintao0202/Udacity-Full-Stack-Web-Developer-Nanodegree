# Review from TA (final submission)
- If you like to push your knowledge a little bit further, check out this Flask [Cheat Sheet](https://s3.us-east-2.amazonaws.com/prettyprinted/flask_cheatsheet.pdf). It really has some nice tips.
- Great job using ilike operator instead of like operator to match case insensitive.
- This [SQLAlchemy cheat sheet](https://www.codementor.io/@sheena/understanding-sqlalchemy-cheat-sheet-du107lawl) is really useful. You can take a look on it as it has some really useful information

# Review from TA (past submission)
- `JOIN`

Your code achieved project's different functionalities without using JOIN queries - which in and of itself are good! To challenge yourself and conform with the rubric, make use of the JOIN query in your next submission.

This is a quick intro to JOIN for SQLAlchemy:
https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join

You can use join query as follows to get the past_shows

`past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()`

- Please create a models.py and copy all your models to that file then use an import statement to import them here, following the principle of separation of concerns.

Your code needs to follow principle of separation of concerns. This is what it is meant when the rubric asks for code to decoupled into relevant parts across the files! You need to define the models in the different file (models.py commonly )separately
Add To Knowledge
Principle of Separation of Concerns
According to Wikipedia:

Separation of Concerns (SoC) is a design principle for separating a computer program into distinct sections such that each section addresses a separate concern. A concern is a set of information that affects the code of a computer program. A concern can be as general as "the details of the hardware for an application", or as specific as "the name of which class to instantiate"

In short :

Don’t write your program as one solid block, instead, break up the code into chunks that are finalized tiny pieces of the system each able to complete a simple distinct job.

So if you are following the principle of separation of concerns then what you will do is that you will define your models in a different file and then the configuration for the database in different files and then different types of routes for the API in a different class, etc and then there will be one file in which you will be adding all these to make the functionality you thought of!

Benefits
Better code clarity. It is much easier to understand what is going on in the program when each module has a concise and clear API with a logically scoped set of methods.
Better code reusability
Better testability. Independent modules with properly scoped functionality and isolation from the rest of the app are a breeze to test
It is easier to organize simultaneous development by multiple engineers. They just need to agree on which module they are working on to make sure they don’t interfere with each other.
FOR EXAMPLE:
Whatever you will do in config.py is putting out the SQL_ALCHEMY_DATABASE_URI and then you will import the same in the file app.py.

This way whenever you intend to change the SQL_ALCHEMY_DATABASE_URI then you will just look for the file config.py and then you are done!

This way you can be more reliable on working with your team because you know what you all have to do is you just need to import SQL_ALCHEMY_DATABASE_URI from the file config.py and the other teammate which is working with config.py will have to just make sure that he/she results out the SQL_ALCHEMY_DATABASE_URI and he/she does not need to worry about anything else going in another files!

- you should have updated your requirements.txt. There were some packages which were not installed in the package and there was so much of it. So i used my requirements.txt. There might be some redundant packages listed in my requirements.txt because i have used some extra packages!

Add To Knowledge
Note - Always make a virtual environment while developing web apps or doing any sort of development. In that way, you are able to isolate your environment from the system. This also helps in listing out the packages installed in that virtual environment.
Please use the command

`pip freeze > requirements.txt`
in order to fill the requirements.txt file

You should list all the packages in your virtual environment by using the command

`pip freeze > requirements.txt`

Please note that if you do not use a virtual environment and then run the above command then the requirements.txt will get populated by the system-wide packages that are installed in the host system which obviously does not make sense!

Once you are done with that then i will be able to build your project and so further review your rubrics!

I hope you understand that! Although everything else is looking as perfect as it should be but since i cannot install all the required packages i cannot be sure and proceed further!

- You can group methods from the same module like so:

from flask import (
Flask,
render_template,
request,
flash,
redirect,
url_for
)

- You can also use the lambda function as can be seen in the following code

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)

  past_shows = list(filter(lambda x: x.start_time < datetime.today(), venue.shows))
  upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), venue.shows))

  past_shows = list(map(lambda x: x.show_artist(), past_shows))
  upcoming_shows = list(map(lambda x: x.show_artist(), upcoming_shows))

  data = venue.venue_to_dictionary()

  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)

  data['upcoming_shows'] = upcoming_shows
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)
  
 To see what error is being thrown, you may:

`print(sys.exc_info())` in `create_venue_submission()`

- Except clause

Add To Knowledge
When catching exceptions, mention specific exceptions whenever possible instead of using a bare except:clause.

For example, use:

 try:
     import platform_specific_module 
 except ImportError:
     platform_specific_module = None
A bare except:clause will catch SystemExitand KeyboardInterrupt exceptions, making it harder to interrupt a program with Control-C, and can disguise other problems. If you want to catch all exceptions that signal program errors, use except Exception:(bare except is equivalent to except BaseException:).

A good rule of thumb is to limit use of bare 'except' clauses to two cases:

If the exception handler will be printing out or logging the traceback; at least the user will be aware that an error has occurred.
If the code needs to do some cleanup work, but then lets the exception propagate upwards with raise. try...finally can be a better way to handle this case

- [ PEP8 guidelines](http://pep8.org/)

For checking whether you meet PEP8 guidelines or not you should checkout the package pycodestyle which you can use to learn what are the things you need to improve upon so that you meet PEP8 guidelines!

Installation
Use pip to install it

pip3 install pycodestyle
After Installation checking in a file the command is

pycodestyle filename.py
In your case it is

pycodestyle app.py
For more on it: Visit this link: https://pypi.org/project/pycodestyle/
Similarly, you can do for all the python files!

Try running for your files and then accordingly make the changes to meet the PEP8 guidelines standards!

- error response

It is recommended to define atleast 4 error handlers in any project

Suggestion
You can define for all these error responses:

bad_request - 400
unauthorized - 401
forbidden - 403
not_found - 404
server_error - 500
not_processable - 422
invalid_method - 405
duplicate_resource - 409

- `format.py` add custom validators

You can define custom validators which will be used in the form to validate the data as follows

##### CUSTOM VALIDATORS ######

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def isNotPast(form,field):
    if field.data < datetime.today():
        raise ValidationError('Start day and time are in the past ! Please fill in a valid value.')

def ifArtistExists(form,field):
    from app import Artist
    if Artist.query.get(field.data) == None:
        raise ValidationError('Artist not listed in our database')

def ifVenueExists(form,field):
    from app import Venue
    if Venue.query.get(field.data) == None:
        raise ValidationError('Venue not liste in our database')

def DuplicateVenueName(form,field):
    ## Check if editing or creating :
    referer = request.headers.get("Referer")
    if referer[-4:] == "edit" :
        pass
    else:
        from app import Venue
        if Venue.query.filter_by(name=field.data).first() != None :
            raise ValidationError('Venue name already existing in the database')

def isImgValid(form,field):

    if len(field.data.rsplit('.', 1))>1:
        ext = field.data.rsplit('.', 1)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError('File extension is not an image')

def DuplicateArtistName(form,field):
    ## Check if editing or creating :
    referer = request.headers.get("Referer")
    if referer[-4:] == "edit" :
        pass
    else:
        from app import Artist
        if Artist.query.filter_by(name=field.data).first() != None :
            raise ValidationError('Artist name already existing in the database')
            
 - Validate phone number
 You can also define a function as follows which will make sure that user is always entering a valid phone number!

# Implementation 1:
def validate_phone(self, phone):
        us_phone_num = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
        match = re.search(us_phone_num, phone.data)
        if not match:
            raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')
.
Alternative Implementation for the function validate_phone using the package phonenumbers

def validate_phone(field):
    if len(field.data) != 10:
        raise ValidationError('Invalid phone number.')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):

.

phone = StringField(
        'phone',
        validators=[DataRequired(), validate_phone] 
    )
Similarly, you can define the function for validating genres!

- `config.py`

You can make a connection this way also by adding a class in the config.py and then importing the same. It gives a better idea of what is going on!

import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

class DatabaseURI:

    # Just change the names of your database and crendtials and all to connect to your local system
    DATABASE_NAME = "fyyur"
    username = 'postgres'
    password = 'postgres'
    url = 'localhost:5432'
    SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        username, password, url, DATABASE_NAME)
 
