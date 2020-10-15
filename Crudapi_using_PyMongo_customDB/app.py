from flask import Flask,Response
from flask_pymongo import PyMongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash
import os

app=Flask(__name__)

@app.route('/')
def ping_server():
    return "Welcome to the world of mine."
try:
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

    mongo = PyMongo(app)
    db = mongo.db
except:
    print("Error - Cannot connect to db")


#try:
#default_connection_url = "mongodb+srv://sam:01521@cluster0.vycaj.mongodb.net/test1?retryWrites=true&w=majority"
#db_name = 'Category'

# create connection
#client = pymongo.MongoClient(default_connection_url)

# create database
#database = client[db_name]

# create collection
#collection_name = 'Employee'
#collection=database[collection_name]

# initially inserted  data
# record={'name': 'iNeuron','description': 'Affordable AI'}         
# collection.insert_one(record)

#print(client.list_database_names())

#except:
#    print("Error - Cannot connect to db")


try:
    @app.route('/add',methods=['POST'])
    def add_employee():
        json=request.json
        name=json['name']
        description=json['description']

        if name and description and request.method=='POST':            
            record_add={'name':name,'description':description}
            db.collection.insert_one(record_add)            
            resp=jsonify('user added successfully'),200
            return resp

        else :
            return 'not_found add_employee'
except:
    print("could not find /add route")


try:
    @app.route('/showall')
    def show_all_employee():
        all_record= db.collection.find()
        record_show=[{"name": rec["name"], "description": rec["description"]} for rec in all_record]
        resp=jsonify('showing data',record_show),200
        return resp
except:
    print("could not find /showall route")


try:
    @app.route('/delete/<id>',methods=['DELETE'])
    def delete_employee(id):
        db.collection.delete_one({"_id":ObjectId(id)})
        return Response(
            response=json.dumps(
               {"message":"Deleted employee","id":f"{id}"}))
except:
    print("could not find /delete route")


try:
    @app.route('/update/<id>',methods=['PATCH'])
    def update_employee(id):
        db.collection.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"],"description":request.form['description']}}
            )

        # for attr in dir(dbResponse):
        #  print(f"********{attr}*******")
        return Response(
            response=json.dumps(
                {"message":"Updated employee","id":f"{id}"}))
except:
    print("could not find update route ")
    
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')