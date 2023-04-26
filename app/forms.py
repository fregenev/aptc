from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User

class ApplyForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already existt! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already existt! Please try a different email address')

    name = StringField(label='Name:', validators=[Length(min=2,max=30), DataRequired()])
    street = StringField(label='Street:', validators=[Length(min=2,max=30), DataRequired()])
    city = StringField(label='City:', validators=[Length(min=2,max=20), DataRequired()])
    lga = StringField(label='Local Government Area:')
    state = StringField(label='State:', validators=[Length(min=2,max=20), DataRequired()])
    country = StringField(label='Country:', validators=[Length(min=2,max=20), DataRequired()])
    qualification = SelectField(label='Highest Education Qualification:', choices=[('BSc', 'Bachelor'), ('MSc','Masters'), ('PhD','Doctorate'), ('HND','Higher National Diploma - HND'), ('NCE','Nigeria Certicate in Education - NCE'), ('OND','National Diploma - OND'), ('Undergraduate','Undergraduate'), ('SSCE','Senior Secondary Certificate Examination'), ('SSStudent','Senior Secondary School Student'), ('Others','Others')] ,validators=[Length(min=2,max=20), DataRequired()])
    subject_area = SelectField(label='Subject Area:', choices=[('Science', 'Science'),('Arts', 'Arts')], validators=[Length(min=2,max=30), DataRequired()])
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirn Password:', validators=[EqualTo('password1'), DataRequired()])
    program_apply = SelectField(label='Program Apply:', choices=[('Python', 'Python programming'), ('DE', 'Data Engineering'),('ML', 'Machine Learning'), ('Webapp', 'Web Application Development with Python'), ('WebDesign', 'Web Design')], validators=[Length(min=2,max=30), DataRequired()])
    start_date = DateField(label='Start Date:', validators=[DataRequired()])
    submit = SubmitField(label='Create Account and Apply')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')