
import os
import json
from flask import (Flask,
                   render_template,
                   request,
                   Response,
                   flash,
                   redirect,
                   url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from config import ALLOWED_ATTACH_EXTENSIONS, ALLOWED_PIC_EXTENSIONS, UPLOAD_CV, UPLOAD_PIC
from forms import *
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct
import datetime
from models import app, db, Employee, Company, Department
from werkzeug.utils import secure_filename


@app.route('/')
def index():
    form = EmployeeForm()
    return render_template('pages/home.html', form=form)


@app.route('/department/create', methods=['GET'])
def get_dept_form():
    form = DeptForm()
    depts = Department.query.all()
    company = Company.query.all()
    form.company_name.choices = [(c.id, c.name) for c in company]
    # pair of id and name , id for backend usage, name to show to user.
    return render_template('pages/create_dept.html', form=form, depts=depts)


@app.route('/department/create', methods=['POST'])
def post_dept_form():
    print(request.form["name"])

    new_dept = Department(
        name=request.form["name"],
        company_id=request.form["company_name"]
    )
    db.session.add(new_dept)
    db.session.commit()
    db.session.close()
    return redirect("/department/create")


@app.route('/company/create', methods=['GET'])
def get_comp_form():
    form = CompForm()
    companies = Company.query.all()
    return render_template('pages/create_comp.html', form=form, companies=companies)


@app.route('/company/create', methods=['POST'])
def post_comp_form():
    form = CompForm()
    error = False
    print(request.form["name"])
    # try:
    # crete object of an Employee model
    new_company = Company(
        name=request.form["name"],
    )
    db.session.add(new_company)
    db.session.commit()
    db.session.close()
    return redirect("/company/create")


@app.route('/employee/create', methods=['GET'])
def get_employee_form():
    form = EmployeeForm(request.form)
    department = Department.query.all()
    form.dept_name.choices = [
        (d.id, d.name+", "+d.companydepartment.name) for d in department]
    # pair of id and name , id for backend usage, name to show to user.
    return render_template('pages/create_employee.html', form=form)


@app.route('/employee/create', methods=['POST'])
def post_employee_submission():
    errors = []
    attach_cv = request.files['attach_cv']
    emp_pic = request.files['emp_pic']

    cv_filename = None
    pic_filename = None

    if attach_cv.filename != "":
        print(allowed_file(attach_cv, "cv"))
        if allowed_file(attach_cv.filename, "cv"):
            cv_filename = secure_filename(attach_cv.filename)
            attach_cv.save(os.path.join(app.config['UPLOAD_CV'], cv_filename))
        else:
            errors = True
            flash("invaild file type for cv")

    if emp_pic.filename != "":
        if allowed_file(emp_pic.filename, "image"):
            pic_filename = secure_filename(emp_pic.filename)
            emp_pic.save(os.path.join(app.config['UPLOAD_PIC'], pic_filename))
        else:
            errors = True
            flash("invaild file type for pic")

    if errors:
        return redirect(url_for("get_employee_form", form=request.form))

    # crete object of an Employee model
    new_employee = Employee(
        name=request.form["name"],
        email=request.form["email"],
        dept_id=request.form["dept_name"],
        basic_salary=request.form["basic_salary"],
        first_allowance=request.form["first_allowance"],
        second_allowance=request.form["second_allowance"],
        attach_cv=cv_filename,
        emp_pic=pic_filename,
        hiring_date=request.form["hiring_date"]
    )
    db.session.add(new_employee)
    db.session.commit()
    db.session.close()
    return redirect("/employee/create")


@app.route('/report', methods=['GET'])
def get_report():
    form = SearchForm()
    employees = Employee.query.all()
    return render_template('pages/report.html', employees=employees, form=form)


@app.route('/report', methods=['POST'])
def post_report():
    form = SearchForm()
    employees = Employee.query.all()
    search = request.form.get("search", "")
    if search != "":
        match request.form["searchfilter"]:
            case 'emp_id':
                if search.isdigit():
                    employees = db.session.query(Employee).filter(
                        Employee.id == search).all()
            case 'emp_name':
                employees = db.session.query(Employee).filter(Employee.name.ilike(
                    f"%{search}%")).all()
            case 'company':
                employees = db.session.query(Employee).filter(Employee.department.has(Department.companydepartment.has(Company.name.ilike(f"%{search}%")))).all()
            case 'department':
                 employees = db.session.query(Employee).filter(Employee.department.has(Department.name.ilike(f"%{search}%"))).all()
            case 'hiring_date':
                 employees = db.session.query(Employee).filter(Employee.hiring_date==search).all()
        
    return render_template('pages/report.html', employees=employees, form=form)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


def allowed_file(filename, tag):
    if tag == "image":
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_PIC_EXTENSIONS
    else:
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_ATTACH_EXTENSIONS

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
