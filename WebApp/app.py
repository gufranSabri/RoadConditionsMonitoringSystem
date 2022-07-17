import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from keras.applications.vgg16 import preprocess_input
from flask import request, jsonify, Flask, render_template, redirect, url_for, session
from flask_cors import CORS, cross_origin

import db_handler as dbh

app = Flask(__name__)
app.secret_key = "super secret key"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cc = 0

def get_model():
    global model
    model = tf.keras.models.load_model('./model/model.h5')
    print(" * Model loaded!")

# def get_image_from_b64(uri):
#    encoded_data = uri.split(',')[1]
#    nparr = np.frombuffer(base64.b64decode(uri), np.uint8)
#    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    img = cv2.resize(img, (224,224))
#    img = img[100:, :]
#    img = img[...,::-1]
#    cv2.imwrite('/media/gufran/GsHDD/Work/Projects/RoadCapture/Dataset/'+str(cc)+'.jpg', img)
#    cc+=1
#    cv2.imshow("img",img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#    img = preprocess_input(img)
#    img = np.expand_dims(img, axis=0)

#    return img

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    # ed = base64.b64encode(image.tobytes())
    image = tf.keras.preprocessing.image.img_to_array(image)
    # ed1 = base64.b64encode(image.tobytes())

    # f = open('/media/gufran/GsHDD/Work/Projects/RoadCapture/WebApp/x.txt','w')
    # f2 = open('/media/gufran/GsHDD/Work/Projects/RoadCapture/WebApp/y.txt','w')

    # f.write(str(ed))
    # f2.write(str(ed))

    image = preprocess_input(image)
    # cv2.imshow("img",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    image = np.expand_dims(image, axis=0)

    return image

def resolve_image(encoded):
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    return preprocess_image(image, target_size=(224, 124))
    

print(" * Loading Keras model...")
get_model()

@app.route("/")
def render_index():
    data= {}
    try:
        res = dbh.get_data(dbh.ROAD_POINT_COLLECTION)

        cc=0
        for p in res:
            cc+=1
            del p["_id"]
            data["point"+str(cc)]=p
    except:
        data={"error":"db"}

    return render_template("index.html", points=data)

@app.route("/login")
def render_login():
    try:
        if session['user'] is not None:
            return redirect(url_for('render_admin'))
    except:
        message="RoadCapture - login"
        try:
            message = session['login_prompt']
        except:
            message="RoadCapture - login"
            pass
        return render_template("login.html", login_prompt=message)

@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    # try:
        username = request.form["username"]
        password = request.form["password"]

        res = dbh.get_data(dbh.USER_COLLECTION)
        for user in res:
            print(user)
            if user["uid"] == username and user["password"] == password:
                session['login_prompt'] = "RoadCapture - login"
                session['user'] = username
                return redirect(url_for('render_admin'))
            else:
                session['login_prompt'] = "Invalid username or password"
                return redirect(url_for('render_login'))
    # except:
        # return jsonify({"error":"error"})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('render_login'))

@app.route("/admin")
def render_admin():
    return render_template("admin.html")

@app.route("/admin", methods=["POST"])
@cross_origin()
def admin():
    message = request.get_json(force=True)

    data={}
    if "user" in message["action"]:
        data = {
            "uid": message["uid"], 
            "password": message["password"], 
            "email": message["email"], 
            "auth": message["auth"]
        }
    else:
        data = {
            "classification": message["classification"], 
            "time": message["time"], 
            "latitude": message["lat"], 
            "longitude": message["lng"], 
            "image": "", 
            "modifiedBy": message["modifiedBy"]
        }
        

    if message["action"] == "add user":
        if len(message["uid"]) < 6:
            return jsonify({"action":"invalid username"})
        if not message["uid"].isalnum():
            return jsonify({"action":"invalid username"})

        if len(message["password"]) < 8:
            return jsonify({"action":"invalid password"})
        if not message["password"].isalnum():
            return jsonify({"action":"invalid password"})

        if message["auth"] == '0':
            return jsonify({"action":"empty"})

        res = dbh.get_data(dbh.USER_COLLECTION)
        for user in res:
            if user["uid"] == message["uid"]:
                return jsonify({"action":"user exists"})
            if user["email"] == message["email"]:
                return jsonify({"action":"email exists"})

        dbh.insert_data(dbh.USER_COLLECTION, data)
    
    #add entry
    elif message["action"] == "add entry":
        dbh.insert_data(dbh.ROAD_POINT_COLLECTION, data)


    return jsonify({"action":"success"})
    
    

@app.route("/predict")
def render_predict():
    return render_template("predict.html")

@app.route("/predict", methods=["POST"])
@cross_origin()
def predict():
    try:
        message = request.get_json(force=True)
        processed_image = resolve_image(message['image'])
        # processed_image = get_image_from_b64(encoded)

        prediction = model.predict(processed_image).tolist()[0]
        ind = prediction.index(max(prediction))

        label=""
        label = "good" if ind == 0 else label
        label = "medium" if ind == 1 else label
        label = "bad" if ind == 2 else label
        label = "unpaved" if ind == 3 else label
        
        response = {
            'predictions': {
                "good": prediction[0],
                "medium": prediction[1],
                "bad": prediction[2],
                "unpaved": prediction[3]
            },
            "prediction": label
        }
        print(prediction)


        data = {
                "classification":label,
                "image":"",
                "time":"lmao",
                "lat":message['latitude'],
                "lng":message['longitude'],
                "modBy":"admin"
            }
        print(data)
        if not message['testing']:
            
            
            dbh.insert_data(dbh.ROAD_POINT_COLLECTION,data)

        return jsonify(response)
    except:
        return jsonify({})

if __name__ == "__main__":
    app.run(debug=True)

'''
in this dir
    export FLASK_APP=app.py
    flask run --host=0.0.0.0
'''