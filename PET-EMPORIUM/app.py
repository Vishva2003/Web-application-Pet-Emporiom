import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import re
import ibm_boto3
from ibm_botocore.client import Config

app = Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Vishva2003',
    database='petapp'
)
cursor = conn.cursor()




@app.route("/")
def home():
    
    return render_template("pethome.html")

#Routing to the user Login page

@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

@app.route("/userlogin1", methods=['GET', 'POST'])
def userlogin1():
    msg =""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']

        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user=cursor.fetchall()
        
        if len(user)>0:
            session["USER_ID"]=user[0][0]
            return redirect("/product")
        else:
            error="Invalid username or password"
            return render_template("userlogin.html", msg=error)
        
    return render_template('userlogin.html')
#Routing to the admin Login page

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")


@app.route("/adminlogin1", methods=['GET', 'POST'])
def adminlogin1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']

        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user=cursor.fetchall()
        
        if len(user)>0:
            session["USER_ID"]=user[0][0]
            return redirect("/product")
        else:
            error="Invalid username or password"
            return render_template("adminlogin.html",msg=error)
        
    return render_template('adminlogin.html')

#Routing to the merchant Login page

@app.route("/merchantlogin")
def merchantlogin():
    return render_template("merchantlogin.html")

@app.route("/merchantlogin1", methods=['GET', 'POST'])
def merchantlogin1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']

        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user=cursor.fetchall()
        
        if len(user)>0:
            session["USER_ID"]=user[0][0]
            return redirect("/product")
        else:
            error="Invalid username or password"
            return render_template("merchantlogin.html",msg=error)
        
    return render_template('merchantlogin.html')
#Routing to user register page


@app.route("/userreg")
def userreg():
    return render_template("userreg.html")

@app.route("/userreg1", methods=['GET', 'POST'])
def userreg1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']
        EMAIL = request.form['email']

        # Check if account exists using MySQL
        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user = cursor.fetchall()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EMAIL):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', USERNAME):
            msg = 'Username must contain only characters and numbers!'
        elif not USERNAME or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            query =("INSERT INTO user(USER_ID,USERNAME ,PASSWORD ,EMAIL ) VALUES (NULL, %s, %s, %s)")  
            cursor.execute(query, (USERNAME, PASSWORD,EMAIL,))
            user=conn.commit()
            msg = 'You have successfully registered!'
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('userreg.html', msg=msg)

#Routing to admin register page

@app.route("/adminreg")
def adminreg():
    return render_template("adminreg.html")

@app.route("/adminreg1", methods=['GET', 'POST'])
def adminreg1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']
        EMAIL = request.form['email']

        # Check if account exists using MySQL
        query = "SELECT * FROM user WHERE USERNAME = %s AND PASSWORD = %s"
        cursor.execute(query, (USERNAME, PASSWORD))
        user = cursor.fetchall()
        # If account exists show error and validation checks
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EMAIL):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', USERNAME):
            msg = 'Username must contain only characters and numbers!'
        elif not USERNAME or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            query =("INSERT INTO user(USER_ID,USERNAME ,PASSWORD ,EMAIL ) VALUES (NULL, %s, %s, %s)")  
            cursor.execute(query, (USERNAME, PASSWORD,EMAIL, ))
            user=conn.commit()
            msg = 'You have successfully registered!'
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('adminreg.html', msg=msg)

#Routing to user home page after login


@app.route("/product")
def product():
    return render_template("product.html")

#Routing to upload after login

@app.route("/pets")
def pets():
    return render_template("pets.html")

@app.route("/pets1", methods=['POST','GET'])
def pets1():
    msg=""
    if request.method=="POST":
        DESCRIPTION = request.form['description']
        PRICE_RANGE = request.form['price_range']
        COMMENTS = request.form['comments']
        
        f=request.files["image"]
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,"uploads",f.filename)
        f.save(filepath)
        # Constants for IBM COS values
        COS_ENDPOINT = "https://s3.us-south.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "PKJi4GNB6i5fbHrtuPol7rMrfCDkiargXENYo9Gh67Ee"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/7583e14b8ab848698452224c4d7b8671:94a47c1d-7d48-4a73-b87d-985f5b18ead5::"
        # Create resource
        cos=ibm_boto3.client("s3",ibm_api_key_id=COS_API_KEY_ID,ibm_service_instance_id=COS_INSTANCE_CRN,config=Config(signature_version="oauth"),endpoint_url=COS_ENDPOINT)
        cos.upload_file(Filename= filepath,Bucket="vishva",key= "useruploads.jpg")
        # current user = session ["USERNAME"]
        query = "SELECT * FROM user WHERE USERID=" + str(session ['USERID'])
        cursor.execute(query)
        user = cursor.fetchall()
        #inserting values
        query1 =("INSERT INTO pets (DESCRIPTION,PRICE_RANGE ,COMMENTS ) VALUES (%s, %s, %s)")  
        cursor.execute(query1, (DESCRIPTION,PRICE_RANGE ,COMMENTS))
        pets=conn.commit()
        msg = 'You have successfully Uploaded!'
        
    return render_template("pets.html")

#Routing to about page

@app.route("/about")
def about():
    return render_template("about.html")

#Routing to logout page

@app.route("/logout") 
def logout():
    session.pop("USER_ID")
    return redirect("/")

#Routing to contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact1", methods=['GET', 'POST'])
def contact1():
    msg=""
    if request.method == 'POST':
        USERNAME = request.form['username']
        EMAIL = request.form['email']
        MESSAGE = request.form['message']

    
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
        query =("INSERT INTO contact (USERNAME ,EMAIL ,MESSAGE) VALUES (%s, %s, %s)")  
        cursor.execute(query, (USERNAME ,EMAIL ,MESSAGE))
        contact=conn.commit()
        msg = 'THANKS for the post!'
    else :
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('contact.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True , port=5000,host= "0.0.0.0")