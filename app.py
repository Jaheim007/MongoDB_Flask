import db
import hashlib
from flask import Flask, request , jsonify
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route("/create" , methods=['POST'])
def create_user():
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email= request.json['email']
        password = request.json['password']
        image = request.json['image']
        
        hide_password = hashlib.md5(password.encode())
        
        acounts = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email, 
            "password": hide_password.hexdigest(), 
            "image": image
        }
        
        db.db.collection.insert_one(acounts)
        return jsonify("User Created")
    
@app.route("/allusers" , methods =['GET'])
def all_acounts():
    database = db.db.collection.find()
    account_list= []
    for users in database:    
        account_dict = {
            "id" : str(ObjectId(users["_id"])),
            "first_name": users['first_name'],
            "last_name" : users['last_name'],
            "email" : users['email'], 
            "password" : users['password'], 
            "image" : users['image'] 
        }
        
        account_list.append(account_dict)
    return jsonify(account_list)

@app.route("/getuser/<_id>" , methods=['GET'])
def getuser(_id):
    users = db.db.collection.find_one({ '_id' : ObjectId(_id)})
    account_dict = {
            "id" : str(ObjectId(users["_id"])),
            "first_name": users['first_name'],
            "last_name" : users['last_name'],
            "email" : users['email'], 
            "password" : users['password'], 
            "image" : users['image'] 
        }
    return jsonify(account_dict)
    
@app.route("/delete/<_id>" , methods =['DELETE'])
def delete_users(_id):
    db.db.collection.delete_one({ '_id' : ObjectId(_id)})
    return jsonify("User deleted succesfully")
    
@app.route("/edit_user/<_id>", methods=['PUT'])
def edit_users(_id):
    
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email= request.json['email']
    password = request.json['password']
    image = request.json['image']
    
    account_dict = {
            'first_name': first_name,
            'last_name' : last_name,
            'email' : email, 
            'password' : password, 
            'image' : image 
    }
    
    db.db.collection.update_one({'_id': ObjectId(_id)}, {'$set': account_dict})
    return jsonify('User has been successfully updated')

@app.route("/login", methods=['GET'])
def login():
    email= request.json['email']
    password = request.json['password']
    
    database = db.db.collection.find({}, {'email' : email , 'password': password})
    
    if email == "":
        return jsonify("Email Field is empty")
    
    if password == "":
        return jsonify("Password Field is empty")
    
    if  email not in database:
        return jsonify("Email doesn't Exists")
    
    if  password not in database:
        return jsonify("Password doesn't Exists")

    return jsonify("You're logged in")    
    
    
    
    

if __name__ == "__main__":
    app.run(debug=True)