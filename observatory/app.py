from flask import Flask
import os
from flask import render_template
from observatory.mongo import *
import re

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return 'hello world'
    #render template with values as arguments?

@app.route('/auth/<rfid_num>')
def auth(rfid_num):
    #Read Number
    print os.getcwd()
    file = open('/home/vagrant/rffid/observatory/static/users/users.txt', 'r')
    for user in file:
        pw = user.split(' ')
        print rfid_num
        print pw[1]
        if str(pw[1].strip()) == str(rfid_num):
            return 'Access granted'
    return "DENIED"



