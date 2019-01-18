from flask import Flask,jsonify,request
from flask_pymongo import PyMongo

app=Flask(__name__)

app.config['MONGO_DBNAME']='people'
app.config['MONGO_URI']='mongodb://bharat:bharat123@ds157864.mlab.com:57864/people'

mongo=PyMongo(app)
users=mongo.db.Users


@app.route('/',methods=['POST'])
def find_pass():
    
    username=request.json['username']
    password=request.json['password']
    query=users.find_one({'username': username})
    if query:
        result={'username':query['username'],'password':query['password']}
        if result['password']==password:
            return jsonify({"message":"Login succesful",
                        "code":"202"}),202
        else:
            return jsonify({"message":"incorrect password","code":"204"}),204
    else:
        return jsonify({"message":"No account with this username"})


@app.route('/join',methods=['POST'])
def create_acc():
   
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    user_id=users.insert({'username':username,'email':email,'password':password})
    user_add_check=users.find_one({'_id': user_id})
    if user_add_check:
        return jsonify({"message":"User added succesfully",
                        "code":"201"}),201
    else:
        return jsonify({"message":"User cannot added"})

if(__name__)=='__main__':
    app.run(host = '0.0.0.0',debug=True)
