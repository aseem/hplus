from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from datetime import datetime
from flask.ext.pymongo import PyMongo
from bson import json_util


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGO_DBNAME'] = 'hacker_news_test'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mongo = PyMongo(app)

# Forms
class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')



# Errors

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index')) # Post/Redirect/Get Pattern

    # get top stories
    stories = mongo.db.top_100.find().sort('rank', 1)
    return render_template('index.html', 
        current_time=datetime.utcnow(), 
        form=form, 
        name=session.get('name'), 
        stories=stories)


@app.route('/api/1.0/hn')
def get_hn():
    stories = mongo.db.top_100.find().sort('rank', 1)
    return json_util.dumps(stories, default=json_util.default)
    
@app.route('/api/ApplicationInstances', methods=['POST'])
def enroll_app():
    result = {}
    result['Id'] = '88f57c04-f197-4bb8-9055-f5486f4dd00a'
    result['OrgId'] = 'aseemoutlook.onmicrosoft.com'
    result['Version'] = request.get_json().get('Version')
    result['Publisher'] = request.get_json().get('Publisher')
    result['Category'] = request.get_json().get('Category')
    result['DeviceId'] = request.get_json().get('DeviceId')
    result['Device-Type'] = request.get_json().get('DeviceType')
    result['Platform'] = request.get_json().get('Platform')
    result['OsVersion'] = request.get_json().get('OsVersion')
    result['PolicyUpdated'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    result['Policy-Version'] = "1.0"
    policies = [
    {
        "Name":"mam.access-recheck-offline-timeout",
        "ValueType":"integer",
        "Value":"0",
        "Default":"720",
        "LowerLimit":0,
        "UpperLimit":720
    },
    {
        "Name":"mam.access-recheck-online-timeout",
        "ValueType":"integer",
        "Value":"0",
        "Default":"720",
        "LowerLimit":0,
        "UpperLimit":720
    },
    {
        "Name":"mam.app-sharing-from-level",
        "ValueType":"integer",
        "Value":"1",
        "Default":"1",
        "LowerLimit":0,
        "UpperLimit":2
    },
    {
        "Name":"mam.app-sharing-to-level",
        "ValueType":"integer",
        "Value":"1",
        "Default":"1",
        "LowerLimit":0,
        "UpperLimit":2
    },
    {
        "Name":"mam.clipboard-sharing-level",
        "ValueType":"integer",
        "Value":"2",
        "Default":"2",
        "LowerLimit":0,
        "UpperLimit":3
    },
    {
        "Name":"mam.data-backup-disabled",
        "ValueType":"boolean",
        "Value":"True",
        "Default":"True"
    },
    {
        "Name":"mam.device-compliance-enabled",
        "ValueType":"boolean",
        "Value":"True",
        "Default":"True"
    },
    {
        "Name":"mam.file-encryption-level",
        "ValueType":"integer",
        "Value":"1",
        "Default":"1",
        "LowerLimit":0,
        "UpperLimit":3
    },
    {
        "Name":"mam.file-sharing-save-as-disabled",
        "ValueType":"boolean",
        "Value":"True",
        "Default":"True"
    },
    {
        "Name":"mam.managed-browser-required",
        "ValueType":"boolean",
        "Value":"True",
        "Default":"True"
    },
    {
        "Name":"mam.pin-enabled",
        "ValueType":"boolean",
        "Value":"True",
        "Default":"True"
    }
    ]

    result['Policies'] = policies

    return json_util.dumps(result, default=json_util.default), 201



@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()
