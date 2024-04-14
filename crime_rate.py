import pickle
import json
import os
import plotly.express as px
import plotly.io as pio
import pandas as pd
from flask import Flask , render_template , request , redirect, url_for , jsonify
from pymongo.mongo_client import MongoClient
import pymongo
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import matplotlib
from flask_cors import CORS
matplotlib.use('agg')


app = Flask(__name__)
CORS(app , resources={"/*": {"origins": "*"}})

uri = "mongodb://localhost:27017"

pop = {'HIMACHAL PRADESH': 6856509,
 'PUNJAB': 27704236,
 'CHANDIGARH': 1054686,
 'UTTARAKHAND': 10116752,
 'HARYANA': 25353081,
 'DELHI': 16753235,
 'RAJASTHAN': 68621012,
 'UTTAR PRADESH': 199581477,
 'BIHAR': 103804637,
 'SIKKIM': 607688,
 'ARUNACHAL PRADESH': 1382611,
 'NAGALAND': 1980602,
 'MANIPUR': 2721756,
 'MIZORAM': 1091014,
 'TRIPURA': 3671032,
 'MEGHALAYA': 2964007,
 'ASSAM': 31169272,
 'WEST BENGAL': 91347736,
 'JHARKHAND': 32966238,
 'ODISHA': 41974218,
 'CHHATTISGARH': 25540196,
 'MADHYA PRADESH': 72597565,
 'GUJARAT': 60383628,
 'DAMAN AND DIU': 242911,
 'DADRA NAGAR HAVELI': 342853,
 'MAHARASHTRA': 112372972,
 'ANDHRA PRADESH': 84665533,
 'KARNATAKA': 61130704,
 'GOA': 1457723,
 'LAKSHADWEEP': 64429,
 'KERALA': 33387677,
 'TAMIL NADU': 72138958,
 'PUDUCHERRY': 1244464,
 'ANDAMAN AND NICOBAR ISLANDS': 379944,
 'JAMMU & KASHMIR': 12548926}

classi = {'Rape': [1.08641582167471e-05, 1.895627822745991e-05, 3.291718750198516e-05],
 'Kidnapping and Abduction': [8.083946887299618e-06,
  1.572821604243339e-05,
  3.322677653795379e-05],
 'Dowry Deaths': [3.4517757038731084e-07,
  3.0421036498316e-06,
  6.745525600681731e-06],
 'Assault on women with intent to outrage her modesty': [1.4331743634718997e-05,
  3.150128339229815e-05,
  5.939791943180268e-05],
 'Insult to modesty of Women': [3.3738111954526423e-07,
  2.748447281848697e-06,
  1.0140832616271623e-05],
 'Cruelty by Husband or his Relatives': [1.2350202337481629e-05,
  3.4540176176759506e-05,
  6.921491325380256e-05],
 'Importation of Girls': [0.0, 0.0, 0.0]}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api():
    return jsonify(  {'key': 'value', 'key2': 'value2'} )


@app.route('/predict',methods=['POST'])
def predict():
        cri = str(request.json["Crime"])
        state = str(request.json["State"])
        print(cri , state)
        
        path = os.path.join(os.getcwd(), 'models', f'{state}{cri}pre') 
        predict = pickle.load(open(path,"rb"))
        a = predict.forecast()
        print(a)
        a = a.tolist()
        a = abs(int(a[0]))
        b = a/pop[state] 
        
        if b<=classi[cri][0]: b = "green (i.e  relatively safe reigon) "
        elif b<=classi[cri][1]: b = "yellow (i.e  relatively stay alert)"
        elif b<=classi[cri][2]: b = "orange (i.e  relatively take  precaution)"
        else : b = "red (i.e  relatively take preventive steps)"
        
                       
        return jsonify( {"Numbers": a,"reigion":b } )
    
    
    
# @app.route("/map",methods=['GET','POST'])
# def map():
#         print("Loading")
        
#         crime_type = request.json.get("Crime")
#         if crime_type:
#             path = os.path.join(os.getcwd(), 'datasets', f'{crime_type}.csv') 
#             data = pd.read_csv(path)
            
#             df = df[["state" , "Crime_rate" , "Crime_no"]]
#             st = df["state"].values.tolist()
#             rat =df["Crime_rate"].values.tolist()
#             num =df["Crime_no"].values.tolist()
            
#             diff = rat.copy()
#             diff.sort()
#             print(diff,rat)
            
#             dic = {}
#             for i in dic: dic[rat] = 10000
#             for i in range(len(diff)):
#                 dic[diff[i]] = min( dic[diff[i]] ,i)
                
#             return jsonify( { st , rat , num , dic })
            
            
@app.route("/map", methods=['POST'])
def map():
    print("Loading")
    
    print("hello")
    
    crime_type = request.json.get("Crime")
    if crime_type:
        path = os.path.join(os.getcwd(), 'datasets', f'{crime_type}.csv') 
        data = pd.read_csv(path)
        
        df = data[["state" , "Crime_rate" , "Crime_no"]]
        st = df["state"].values.tolist()
        rat = df["Crime_rate"].values.tolist()
        num = df["Crime_no"].values.tolist()
        
        diff = rat.copy()
        diff.sort()
        print(diff, rat)
        
        dic = {}
        for i in diff: 
            dic[i] = 10000
        for i in range(len(diff)):
            dic[diff[i]] = min(dic[diff[i]], i)
            
        ret = {}
        for i in range(len(st)):
            ret[st[i]] = [ rat[i] , num[i] , dic[rat[i]] ] 
            
        response = jsonify({"map_data": ret})
        response.headers.add("Access-Control-Allow-Origin", "*")           
            
        return response
    return jsonify({"error": "Crime type not provided"}), 400
            
            

@app.route("/comment", methods=['POST'] )
def comment():
        user = request.json.get("user")
        email = request.json.get("email")
        comment = request.json.get("comment")
        client = MongoClient(uri)
        db = client["crimerate"]
        data = {
         "name" : user,
         "email": email ,
         "comment" : comment  
                }
        coll = db["coments"]
        coll.insert_one(data)
        print(user , email ,comment )
        response1 = jsonify({"ok": True})
        response1.headers.add("Access-Control-Allow-Origin", "*")    
        return  response1 
    
    
    
    
@app.route("/visual" ,  methods=['GET','POST'])
def visual():
    if request.method == 'GET':
        return render_template("visual.html")
    crime_type = request.json.get("Crime")
    State = request.json.get("State")
    plot = request.json.get("plot")
    
    df = pd.read_csv(os.path.join(os.getcwd(), 'static', 'crimedata.csv'))
    df = df[["STATE/UT" , "Year" , crime_type ]]
    df = df[df["STATE/UT"] == State]
    x = df["Year"].values
    y = df[crime_type].values
    
    x = x.tolist()
    y = y.tolist()
    
    data = []
    
    for i in range(len(x)):
        dic = {"X": x[i],"value":y[i]}
        data.append(dic)
    
    return jsonify({ "visual" : data })
    

if __name__ == "__main__":
    app.run(debug=True)




