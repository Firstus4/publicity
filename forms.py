from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SelectMultipleField, SubmitField, DateField, TelField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileAllowed, FileField

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=150)])
    middle_name = StringField('Middle name', validators=[Length(max=150)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=150)])
    sex = SelectField('Gender', choices=[('', 'Select'), ('Male','Male'),('Female','Female')], validators=[DataRequired()])
    state = SelectField('State of Origin', choices=[], validators=[DataRequired()])
    lga = SelectField('Local Government Area', choices=[], validators=[DataRequired()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    country_code = SelectField('Country Code', choices=[], validators=[DataRequired()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=7, max=12, message="Phone number must be between 7-12 digits")])
    ppa = StringField('PPA', validators=[DataRequired()])
    school = SelectField('School', choices=[], validators=[DataRequired()], validate_choice=False)
    unit = SelectMultipleField('Church Unit', choices=[], validators=[DataRequired()])
    room_allocated = StringField('Room Allocated', validators=[DataRequired()])
    photo = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only image files are allowed!')])
    submit = SubmitField('Register')
    
    def validate_unit(self, field):
        if len(field.data) > 3:
            raise ValidationError('You can select a maximum of 3 units')
        if len(field.data) == 0:
            raise ValidationError('Please select at least one unit')

class AdminLoginForm(FlaskForm):
    email = StringField('Admin Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class AdminRegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(), Length(max=150)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')
