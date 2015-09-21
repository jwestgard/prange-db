import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://prangedb_admin:admin@localhost/prangedb'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'temporary secret key string'

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, index=True)
    users = db.relationship('User', backref='role')
    
    def __repr__(self):
        return '<Role {0}>'.format(self.username)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User {0}>'.format(self.username)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), 
        current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manager.run()

