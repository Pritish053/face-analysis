from flask import Flask                             
from flask import render_template, request, redirect, url_for, flash , url_for, session  ,jsonify              
from flaskext.mysql import MySQL                    
from datetime import datetime
import os
from flask import send_from_directory
import logging
from functools import wraps
import base64
import requests
import json
from deepface import DeepFace


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)                               
app.secret_key="mySecteKeyASDFG"
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='faceanalysis'
mysql.init_app(app)                                 

folder = os.path.join("uploads")
app.config["folder"] = folder
mlservice_api = False

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return render_template('admin/login.html')
    return wrap

@app.route("/")
def index():
    return redirect(url_for("create"))

@app.route("/special/uploads/<nombreFoto>")
def uploads(nombreFoto):
    return send_from_directory(app.config["folder"], nombreFoto)

@app.route('/admin/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('special'))
    return render_template('admin/login.html')


@app.route("/special/")    
@login_required                              
def special():
    sql = "SELECT * FROM `faceanalysis`.`users`;"
    conn=mysql.connect()                            
    cursor=conn.cursor()                            
    cursor.execute(sql)                             
    user_data = cursor.fetchall()
    conn.commit()                                   
    return render_template("crud/index.html", user_data=user_data)  

@app.route("/admin/login", methods=['GET', 'POST'])                                     
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connect().cursor()
        cursor.execute('SELECT * FROM `faceanalysis`.`admin` WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            print(account)
            session['loggedin'] = True
            session['id'] , session['username'] , _ = account
            # session['username'] = account['username']
            return redirect(url_for('special'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            return render_template('admin/login.html', msg=msg)

@app.route('/admin/logout')
@login_required
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('home'))
		

@app.route("/destroy/<int:id>")
@login_required
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT photo FROM `faceanalysis`.`users` WHERE id=%s", id)
    cursor_data = cursor.fetchall()
    app.logger.info(os.path.join(app.config["folder"], cursor_data[0][0]))
    os.remove(os.path.join(app.config["folder"], cursor_data[0][0]))
    cursor.execute("DELETE FROM `faceanalysis`.`users` WHERE id=%s", (id))
    conn.commit()
    return redirect(url_for("special"))

@app.route("/edit/<int:id>")
@login_required
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `faceanalysis`.`users` WHERE ID=%s", (id))
    user_data = cursor.fetchall() 
    conn.commit()
    return render_template("crud/edit.html", user_data = user_data)

@app.route("/update", methods=["POST"])
@login_required
def update():
    _name = request.form["form_name"]
    _email = request.form["form_email"]
    _photo = request.files["form_photo"]
    id = request.form["txtID"]
    sql = "UPDATE `faceanalysis`.`users` SET `name`=%s, `email`=%s WHERE id=%s;"
    sql_data = (_name, _email, id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, sql_data)
    conn.commit()
    now = datetime.now()
    timeStamp = now.strftime("%Y%H%M%S")
    if _photo.filename != "":
        newPhotoName = timeStamp + _photo.filename
        _photo.save("uploads/" + newPhotoName)
        cursor.execute("SELECT photo FROM `faceanalysis`.`users` WHERE id=%s", id)
        cursor_data = cursor.fetchall()
        os.remove(os.path.join(app.config["folder"], cursor_data[0][0]))
        cursor.execute("UPDATE `faceanalysis`.`users` SET photo=%s WHERE id=%s", (newPhotoName, id))
        conn.commit()
    return redirect(url_for('home'))

@app.route('/create') 
def create(): 
    return render_template('crud/create.html')

@app.route("/store", methods=["POST"])
def storage():
    _name = request.form['form_name'] 
    _email = request.form['form_email'] 
    _photo = request.files['form_photo']
    if _name == '' or _email == '' or _photo.filename =='': 
        flash('Please fill in all required fields !!') 
        return redirect(url_for('create'))
    now = datetime.now()
    timeStamp = now.strftime("%Y%H%M%S")
    if _photo.filename != "":
        newPhotoName = timeStamp +"_"+ _name + "_" +_photo.filename
        _photo.save("uploads/" + newPhotoName)
        img_path = "uploads/" + newPhotoName
    if mlservice_api:
        DeepFaceOBJ = analyze(img_path)
        if DeepFaceOBJ is None:
            flash('Please upload a valid photo !!') 
            return redirect(url_for('create'))
    else:
        try:
            DeepFaceOBJ = DeepFace.analyze(img_path = img_path, actions = ['age', 'gender'],detector_backend = "mediapipe")
        except Exception as e:
            flash('Please upload a valid photo !!')
            return redirect(url_for('create'))
    _age = DeepFaceOBJ.get('age')
    _gender = DeepFaceOBJ.get('gender')
    _time = now.strftime("%d/%m/%Y %H:%M:%S")
    sql = "INSERT INTO `faceanalysis`.`users` (`id`, `name`, `email`,`age`, `gender`,`time` ,`photo`) VALUES (NULL, %s, %s, %s,%s, %s, %s);" 
    sql_data = (_name, _email,_age,_gender,_time ,newPhotoName)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, sql_data)                      
    conn.commit()
    flash('''Hi {},
          Here is your result :  
          Age: {} 
          Gender: {} 
          Time : {}'''.format(_name,_age, _gender,_time))
    return redirect('/create')

def analyze(image_path):
    print(image_path)
    with open(image_path, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    print("hello")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps( { "img": ["data:image/jpeg;base64,"+ im_b64]})
    print("hello2")
    response = requests.post('http://20.197.30.158:5010/analyze', data=payload, headers=headers)
    print("hello3")
    try:
        data = response.json()
        print(data)
        return data
    except requests.exceptions.RequestException:
        print(response.text)
        return None

if __name__=="__main__":                             
    app.run(debug=True)                             

