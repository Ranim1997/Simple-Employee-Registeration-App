from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)


class Employee(db.Model):
    __tablename__ = 'Employee'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String(120))
    emp_pic = db.Column(db.String(500))
    basic_salary = db.Column(db.Integer)
    first_allowance=db.Column(db.Integer)
    second_allowance=db.Column(db.Integer)
    attach_cv=db.Column(db.String(500))
    hiring_date = db.Column(db.Date)
    dept_id  = db.Column(db.Integer, db.ForeignKey("Department.id"),  nullable=False)
    department = db.relationship("Department", back_populates="employee")
    @hybrid_property
    def total_salary(self):
        return self.basic_salary + (self.basic_salary*(self.first_allowance/100)) + (self.basic_salary*(self.second_allowance/100))
    pass


class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    # relation for company to have many departments
    departs = db.relationship('Department', backref="companydepartment")
    pass

class Department(db.Model):
    __tablename__ = 'Department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    company_id  = db.Column(db.Integer, db.ForeignKey("Company.id"),  nullable=False)

    employee = db.relationship(
        "Employee", uselist=False,
        back_populates="department"
    )

    pass

