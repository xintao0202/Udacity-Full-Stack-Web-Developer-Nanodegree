from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError, Optional
from flask import request, flash
import re
from models import Artist, Show, Venue


##### CUSTOM VALIDATORS ######
# https://hackersandslackers.com/flask-wtforms-forms/
# Need change html to show error msg https://knowledge.udacity.com/questions/157388
# need to import ValidationError from WTFforms and also edit app.py https://knowledge.udacity.com/questions/77530

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
genres=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
Genre_list1, Genre_list2 = zip(*genres)

def isNotPast(form,field):
    if field.data < datetime.today():
        raise ValidationError('Start day and time are in the past ! Please fill in a valid value.')

def ifArtistExists(form,field):
    
    if Artist.query.get(field.data) == None:
        raise ValidationError('Artist not listed in our database')

def ifVenueExists(form,field):
    if Venue.query.get(field.data) == None:
        raise ValidationError('Venue not listed in our database')

def DuplicateVenueName(form,field):
    ## Check if editing or creating :
    referer = request.headers.get("Referer")
    if referer[-4:] == "edit" :
        pass
    else:
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
        if Artist.query.filter_by(name=field.data).first() != None :
            raise ValidationError('Artist name already existing in the database')

# custome phone validator:
def validate_phone(form,field):
    us_phone_num = '^([0-9]{3})[-][0-9]{3}[-][0-9]{4}$'
    match = re.search(us_phone_num, field.data)
    if not match:
        raise ValidationError('Error, phone number must be in format xxx-xxx-xxxx')


# custom genre validator:
def validate_genre(form, field):
        for option in field.data:
            if option not in Genre_list1:
                raise ValidationError('Invalid value, must be one of: %s' % ([value for value in Genre_list1]))

class ShowForm(Form):
    artist_id = StringField(
        'artist_id', 
        validators=[DataRequired(), ifArtistExists]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired(), ifVenueExists]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(), isNotPast],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired(), DuplicateVenueName]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[validate_phone]
    )
    image_link = StringField(
        'image_link',
        validators=[Optional(), isImgValid]
    )
    genres = SelectMultipleField(
        # implementation enum restriction
        'genres', validators=[DataRequired(), validate_genre],
        choices=genres
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    website = StringField(
            'website', validators=[Optional(), URL()]
        )
    seeking_talent = BooleanField(
            'seeking_talent'
        )
    seeking_talent_ad = TextAreaField(
            'What kind of Talent are you seeking for'
        )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired(), DuplicateArtistName]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # implement validation logic for state
        'phone', validators=[DataRequired(), validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), isImgValid]
    )
    genres = SelectMultipleField(
       # implementation enum restriction
        'genres', validators=[DataRequired(), validate_genre],
        choices=genres
    )
    facebook_link = StringField(
        
        'facebook_link', validators=[Optional(), URL()]
    )

# IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
    website = StringField(
            'website', validators=[Optional(), URL()]
        )
    seeking_venue = BooleanField(
            'seeking_venue'
        )
    seeking_venue_ad = TextAreaField(
            'What venue are you seeking for'
        )