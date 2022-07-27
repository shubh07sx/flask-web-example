from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from flask_wtf.file import FileField


class RegistrationForm(FlaskForm):
	username = StringField('Username', 
		 					validators=[DataRequired(),Length(min=2,max=20)])	
	email = StringField('Email', 
							validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):	
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UploadFileForm(FlaskForm):
	file = FileField("File",validators=[InputRequired()])
	submit = SubmitField('Upload File')

class FilterByCityForm(FlaskForm):
	city_name = StringField('City Name',validators=[DataRequired()])
	submit = SubmitField('Filter!!!')

class FilterByPriceForm(FlaskForm):
	total_price_range = IntegerField('Total price range',validators=[DataRequired()])
	submit = SubmitField('Filter!!!')

class FilterByQuantityForm(FlaskForm):
	quantity_range = IntegerField('Quantity Range',validators=[DataRequired()])
	submit = SubmitField('Filter!!!')

class FilterByDateForm(FlaskForm):
	date_range = StringField('Date Range',validators=[DataRequired(),Length(min=2,max=20)])
	submit = SubmitField('Filter!!!')