from flask import Flask, request, render_template
from datetime import datetime
import pymongo
import os
from config import *

os.environ['MONGO'] = MONGO
Mongo = os.environ.get('MONGO')
client = pymongo.MongoClient(Mongo)
### cluster:ShradhaLearn database:test collection:flask-signup ###
db = client.test
collection = db['flask-signup']

app = Flask(__name__)
@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    ### sending data from backend to frontend using jinja template in the html file ####
    return render_template('index.html',day_of_week=day_of_week)

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form) #Take data entered in the form
    collection.insert_one(form_data) #Accepts only dictionary --> NoSql works with json
    return 'Data Added to mongoDB'

@app.route('/data')
def data():
    content = list(collection.find())
    for elm in content:
        del(elm['_id'])
    return {
        'Content': content
    }

if __name__ == '__main__':
    app.run(debug=True)


'''
fetch using URL. example: http://127.0.0.1:5000/24/30
OUTPUT:
{
  "sum": 54
}
@app.route('/<num1>/<num2>')
def sum(num1,num2):
    sum = int(num1) + int(num2)
    return {
        "sum": sum
    }


fetch using json. example: http://127.0.0.1:5000/api?name=shradha&age=25
OUTPUT:
{
  "age": 25, 
  "name": "shradha"
}
@app.route('/api')
def name():
    name = request.values.get('name')
    age = int(request.values.get('age'))
    result = {
        'name': name,
        'age': age
    }
    return result
'''