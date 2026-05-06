from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
db = SQLAlchemy(app)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    employees = db.relationship('Employee', backref='department')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Float)

    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

with app.app_context():
    db.create_all()

    d1 = Department(name="IT")
    d2 = Department(name="HR")

    e1 = Employee(name="Ali", salary=1000, department=d1)
    e2 = Employee(name="Vali", salary=1200, department=d1)
    e3 = Employee(name="Sami", salary=800, department=d2)

    db.session.add_all([d1, d2, e1, e2, e3])
    db.session.commit()

    # ENG KO'P OYLIK
    max_salary = db.session.query(func.max(Employee.salary)).scalar()
    print("Max salary:", max_salary)

    # DEPARTMENT BO'YICHA O'RTACHA
    avg = db.session.query(Department.name, func.avg(Employee.salary))\
        .join(Employee).group_by(Department.id).all()

    for dept, avg_salary in avg:
        print(dept, avg_salary)
