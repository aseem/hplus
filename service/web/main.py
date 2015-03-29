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
#mongo = PyMongo(app)

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
    

@app.route('/StatelessApplicationManagementService/ApplicationInstances', methods=['POST'])
def enroll_mam():
    result = {}

    print request.get_json()

    result['Key'] = '651a7e38-e85b-4f58-ad12-918adeb41750'
    result['AppId'] = request.get_json().get('AppId')
    result['AppVersion'] = request.get_json().get('AppVersion')
    result['SdkVersion'] = request.get_json().get('SdkVersion')
    result['DeviceId'] = request.get_json().get('DeviceId')
    result['DeviceType'] = request.get_json().get('DeviceType')
    result['DeviceHealth'] = request.get_json().get('DeviceHealth')
    result['Os'] = request.get_json().get('Os')
    result['OsVersion'] = request.get_json().get('OsVersion')
    result['EnrollmentTime'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    result['Action'] = 'http://54.243.48.46/StatelessApplicationManagementService/ApplicationInstances(guid\'651a7e38-e85b-4f58-ad12-918adeb41750\')/Action'

    return json_util.dumps(result, default=json_util.default), 201

@app.route('/StatelessApplicationManagementService/ApplicationInstances(guid\'651a7e38-e85b-4f58-ad12-918adeb41750\')/Action', methods=['GET'])
def checkin_mam():
    result = {}
    result['Key'] = '651a7e38-e85b-4f58-ad12-918adeb41750'
    result['StatusCode'] = 5

    # Action Version Dict
    action_version = {}
    action_version['Major'] = 1
    action_version['Minor'] = 11
    result['PolicyVersion'] = action_version

    # Configuration Dict
    config = [
    {
        "Name":"CheckInOnLaunch",
        "Value":"true",
    },
    {
        "Name":"CheckInInterval",
        "Value":"1",
    }]
    result['Configuration'] = config

    result['Commands'] = []

    # policy dict
    policy = [
        {
            "Name": "PINEnabled",
            "Value": "True"
        },
        {
            "Name": "PINNumRetry",
            "Value": "5"
        },
        {
            "Name": "BlockScreenCapture",
            "Value": "True"
        },
        {
            "Name": "FileSharingSaveAsDisabled",
            "Value": "True"
        },
        {
            "Name": "DataBackupDisabled",
            "Value": "True"
        },
        {
            "Name": "DeviceComplianceEnabled",
            "Value": "False"
        },
        {
            "Name": "RequireFileEncryption",
            "Value": "True"
        },
        {
            "Name": "AuthenticationEnabled",
            "Value": "False"
        },
        {
            "Name": "AccessRecheckOnlineTimeout",
            "Value": "30"
        },
        {
            "Name": "AccessRecheckOfflineTimeout",
            "Value": "720"
        },
        {
            "Name": "AppSharingToLevel",
            "Value": "1"
        },
        {
            "Name": "AppSharingFromLevel",
            "Value": "2"
        },
        {
            "Name": "ClipboardSharingLevel",
            "Value": "2"
        },
        {
            "Name": "FileEncryptionLevel",
            "Value": "3"
        },
        {
            "Name": "MinOsVersion",
            "Value": "7.0"
        },
        {
            "Name": "MinAppVersion",
            "Value": "1.10"
        }
    ]
    result['Policy'] = policy

    return json_util.dumps(result, default=json_util.default), 200


@app.route('/NoPolicy/StatelessApplicationManagementService/ApplicationInstances(guid\'651a7e38-e85b-4f58-ad12-918adeb41750\')/Action', methods=['GET'])
def checkin_no_policy():
    result = {}
    result['Key'] = '651a7e38-e85b-4f58-ad12-918adeb41750'
    result['StatusCode'] = 5

    # Action Version Dict
    action_version = {}
    action_version['Major'] = 1
    action_version['Minor'] = 11
    result['PolicyVersion'] = action_version

    # Commands Dict
    commands = [
        {
            "Name":"NoPolicy",
            "Value":"foo"
        }
    ]
    result['Commands'] = commands



    # Configuration Dict
    config = [
    {
        "Name":"CheckInOnLaunch",
        "Value":"true",
    },
    {
        "Name":"CheckInInterval",
        "Value":"1",
    }]
    result['Configuration'] = config


    # policy dict
    policy = []
    result['Policy'] = policy

    return json_util.dumps(result, default=json_util.default), 200


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
    },
    {
        "Name":"mam.pin-num-retries",
        "ValueType":"integer",
        "Value":"5",
        "Default":"5",
        "LowerLimit":1,
        "UpperLimit":10
    }
    ]

    result['Policies'] = policies

    return json_util.dumps(result, default=json_util.default), 201


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()
