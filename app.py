import os
from flask import Flask, jsonify, request, make_response
import sqlalchemy
from flask_migrate import Migrate
from sqlalchemy import desc

#Importing db and model(s)
from models import db, Course, Students

app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)

@app.route('/students/add', methods=["POST"])
def add():
    if request.method == "POST":
        info= request.get_json() or {}
        item= Students(first_name=info["first_name"],last_name=info["last_name"],age=info["age"],course_id=info["course_id"])
        if info["first_name"] == "":
            return make_response(jsonify({"error": 400, "message":"Bad Request. No first_name" }))
        elif info["last_name"] == "":
            return make_response(jsonify({"error": 400, "message":"Bad Request. No last_name" }))
        elif info["age"] == "":
            return make_response(jsonify({"error": 400, "message":"Bad Request. No age" }))
        elif info["course_id"] == "":
            return make_response(jsonify({"error": 400, "message":"Bad Request. No course_id" }))
        else:
            db.session.add(item)
            db.session.commit()
            return jsonify({"response": "ok"})
    
@app.route('/course/add', methods=["POST"])
def addCourse():
    info= request.get_json() or {}
    item= Course(name=info["name"])
    if info["name"] == "":
        return make_response(jsonify({"error": 400, "message":"Bad Request. No course name"}))
    else:
        db.session.add(item)
        db.session.commit()
        return jsonify({"response": "ok"})


@app.route('/students')
def hello():
    items = Students.query.all()
    response =[]
    for i in items:
        brochacho = i.to_dict()
        response.append(brochacho)
    return jsonify({"data": response})
  
@app.route('/courses')
def courses():
    courses = Course.query.all()
    response = []
    for c in courses:
        course = c.to_dict()
        response.append(course)
    
    return jsonify({"data": response})
 
@app.route('/students/<int:id>', methods=["GET","PUT"])
def get_student(id):
    if request.method == "GET":
        ele = Students.query.get(id)
        stud = ele.to_dict()
        if id > 0:
            return jsonify({"status_code": 200, "data": stud})
    else:
        info= request.get_json() or {}
        ele = Students.query.get(id)
        ele.first_name=info["first_name"]
        ele.last_name=info["last_name"]
        ele.age=info["age"]
        ele.course_id=info["course_id"]
        db.session.commit()
        return jsonify({"response": "ok"})
            
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response  
 
 
@app.route('/courses/<int:id>')   
def get_course(id):
    ele = Course.query.get(id)
    subject = ele.to_dict()
    if id > 0:
                
        return jsonify({"status_code": 200, "data": subject})
    
            
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response 
  
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))