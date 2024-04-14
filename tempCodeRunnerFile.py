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
        
        if b<=classi[cri][0]: b = " green (i.e  relatively safe reigon) "
        elif b<=classi[cri][1]: b = "yellow (i.e  relatively stay alert)"
        elif b<=classi[cri][2]: b = "orange (i.e  relatively take  precaution)"
        else : b = "red (i.e  relatively take preventive steps)"
        
                       
        return jsonify( {"Numbers": a,"reigion":b } )
    