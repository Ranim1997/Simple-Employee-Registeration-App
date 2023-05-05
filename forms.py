from datetime import datetime
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, IntegerField, DateField
from wtforms.validators import DataRequired, AnyOf, URL, Optional, Length
from enum import Enum, auto
from flask_wtf.file import FileField, FileAllowed, FileRequired

class EmployeeForm(Form):

    name = StringField(
        'name', validators=[DataRequired()]
    )
    email = StringField(
        'email', validators=[Optional(), Length(1, 120)]
    )

    dept_name = SelectField(
        'dept_name', validators=[DataRequired()]
    )

    basic_salary = IntegerField(
        'basic_salary', validators=[DataRequired()]
    )
    first_allowance = IntegerField(
        'first_allowance', validators=[DataRequired()]
    )
    second_allowance = IntegerField(
        'second_allowance', validators=[DataRequired()]
    )
    attach_cv = FileField('file', validators=[
        FileAllowed(['pdf'], 'PDF only!')
    ])
    emp_pic = FileField('image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    hiring_date = DateField(
        'hiring_date',
        validators=[DataRequired()],
        default= datetime.today()
    )

class DeptForm(Form):

    name = StringField(
        'name', validators=[DataRequired()]
    )

    company_name = SelectField(
        'company_name', validators=[Optional()]
    )

class CompForm(Form):

    name = StringField(
        'name', validators=[DataRequired()]
    )

class SearchForm(Form):
    search_choices=[('emp_id','Employee ID'), 
                    ('emp_name','Emp Name'), 
                    ('company','Company'), 
                    ('department','Department'), 
                    ('hiring_date','Hiring date')]

    search = StringField(
        'search', validators=[Optional()]
    )
    searchfilter = SelectField(
        'searchfilter', validators=[Optional()], choices=search_choices
    )
    
