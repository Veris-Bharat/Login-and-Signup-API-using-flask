from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app=Flask(__name__)

app.config['MONGO_DBNAME']='people'
app.config['MONGO_URI']='mongodb://bharat:bharat123@ds157864.mlab.com:57864/people'

mongo=PyMongo(app)
users=mongo.db.Users


@app.route('/getusers',methods=['GET'])
def find_all_user():
    result=[]
    for item in users.find():
        stri=item["username"]
        #stri=stri.encode('ascii')
        result.append(stri)
    return jsonify({"usernames":result})

@app.route('/login',methods=['POST'])
def find_pass():
    email=request.json['email']
    password=request.json['password']
    if email is None or password is None:
        return jsonify({"message":"Bad Request","code":"400"}),400
    else:
        query=users.find_one({'email': email})
        if query:
            result={'email':query['email'],'password':query['password']}
            if result['password']==password:
                return jsonify({"message":"Login succesful","code":"200"}),200
            else:
                return jsonify({"message":"Unauthorized Access","code":"401"}),401
        else:
            return jsonify({"message":"No account with this email","code":"404"}),404

@app.route('/join',methods=['POST'])
def create_acc():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']
    user_email_exist_check=users.find_one({'email': email})
    user_username_exist_check=users.find_one({'username': username})
    if user_email_exist_check or user_username_exist_check:
        return jsonify({"message":"Username or Email already exist","code":"409"}),409
    else:
        user_id=users.insert({'username':username,'email':email,'password':password,"posts":[]})
        user_add_check=users.find_one({'_id': user_id})
        if user_add_check:
            return jsonify({"message":"User added succesfully","code":"201"}),201
        else:
            return jsonify({"message":"User cannot added due to internal error","code":"500"}),500

if(__name__)=='__main__':
    app.run(host='0.0.0.0',debug=True)
