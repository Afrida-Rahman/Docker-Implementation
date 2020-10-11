from flask import Flask,Response
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify,request
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)

@app.route('/')
def ping_server():
    return "Welcome to the world of mine."


default_connection_url = "mongodb+srv://user:password@cluster0.vycaj.mongodb.net/test1?retryWrites=true&w=majority"
db_name = 'Category'

client = pymongo.MongoClient(default_connection_url)
database = client[db_name]
collection_name = 'Employee'
collection=database[collection_name]


try:
    @app.route('/add',methods=['POST'])
    def add_employee():
        json=request.json
        name=json['name']
        description=json['description']

        if name and description and request.method=='POST':            
            record_add={'name':name,'description':description}
            collection.insert_one(record_add)            
            resp=jsonify('user added successfully'),200
            return resp

        else :
            return 'not_found add_employee'
except:
    print("could not find /add route")


try:
    @app.route('/showall')
    def show_all_employee():
        all_record= collection.find()
        record_show=[{"name": rec["name"], "description": rec["description"]} for rec in all_record]
        resp=jsonify('showing data',record_show),200
        return resp
except:
    print("could not find /showall route")


try:
    @app.route('/delete/<id>',methods=['DELETE'])
    def delete_employee(id):
        collection.delete_one({"_id":ObjectId(id)})
        return Response(
            response=json.dumps(
               {"message":"Deleted employee","id":f"{id}"}))
except:
    print("could not find /delete route")


try:
    @app.route('/update/<id>',methods=['PATCH'])
    def update_employee(id):
        collection.update_one(
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