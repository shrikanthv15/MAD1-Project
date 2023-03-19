from flask import Flask, render_template, request, flash,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import DataRequired
import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MAD1_PROJECT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adminDB.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

conn = sqlite3.connect('admin.db', check_same_thread=False)
cursor = conn.cursor()

class AdminForm(FlaskForm):
    admin_username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = AdminForm()
    admin_username = None
    admin_password=None
    if (form.validate_on_submit()):
        admin_username = form.admin_username.data
        admin_password = form.password.data

        db_password = cursor.execute(
            "select password from adminLogin where username = '"+admin_username+"'").fetchone()
        if(db_password == None or db_password[0]!=admin_password):
            flash('Login Unsuccessful')
        elif(str(admin_password) == str(db_password[0])):
            return render_template('addvenue.html', name=db_password)
    admin_username=''
    admin_password=''
    return render_template('admin_login.html', form=form, name=admin_username)


@app.route('/admin-dashboard',methods=['GET','POST'])
def adminDashboard():
    return render_template('adminDashboard.html')

@app.route("/addvenue")
def addvenue():
    return render_template('addvenue.html')

@app.route("/admin-dashboard")
def admindashboard():
    return render_template('new.html')