from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
#app.secret_key='secretkey'
app.config['MONGO_URI']="mongodb://localhost:27017/db_for_crudapp"

mongo=PyMongo(app)

@app.route('/add',methods=['POST'])
def add_user():
    json=request.json
    name=json['name']
    email=json['email']
    password=json['pwd']

    if name and email and password and request.method=='POST':
        hashed_password=generate_password_hash(password)
        id = mongo.db.user.insert({'name':name,'email':email,'pwd':hashed_password})
        resp=jsonify('user added successfully')
        resp.status_code=200
        return resp

    else :
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'NOT FOUND'+ request.url
    }

    resp=jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/users')
def users():
    user=mongo.db.user.find()
    resp=dumps(users)
    return resp

@app.route("/user/<id>")
def user(id):
    user = mongo.db.user.find_one({'id':ObjectId(id)})
    resp=dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({"id":ObjectId(id)})
    resp=jsonify('user deleted successfully')
    resp.status_code =200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    id=id
    json=request.json
    name=json['name']
    email=json['email']
    password=json['pwd']
    
    if name and email and password and request.method=='PUT':
        hashed_password=generate_password_hash(password)
        mongo.db.user.update_one({'id':ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},{'$set':{'name':name,'email':email,'pwd':hashed_password}})
        resp=jsonify('user updated successfully')
        resp.status_code=200
        return resp

    else :
        return not_found()

    
if __name__ == "__main__":
    app.run(debug=True)


