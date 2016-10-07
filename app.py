'''Chloe Delfau
SoftDev1 pd 8
HW 05 -- The Greatest Flask App In The World
2016-10-06''' 

#import the necessary libraries from Flask
from flask import Flask, render_template, request
import hashlib
import csv

#create flask app
app = Flask(__name__)
#create a dict
data = dict()

#home route
@app.route("/")
def home():
    #read the file
    readFile()
    #return a login page
    return render_template("login.html")

#register route
@app.route("/register", methods=['POST'])
def register():
    #get the username
    usr = request.form["usr"]
    #get the password
    pw = request.form["pw"]
    #if either username or password is empty, do not authenticate
    if usr == "" or pw == "":
        return "<center>Please fill in all info!</center>"
    #there can only be one of each username, butt ehy can all have the same password!
    elif usr in data:
        return "<center>Username already exist!</center>"
    #otherwise, all is good! to the csv file, as add the username and the hashed password
    else:
        hashObj = hashlib.sha1()
        hashObj.update(pw)
        postPw = hashObj.hexdigest()
        writeFile(usr,postPw)
        readFile()
        return render_template("register_success.html")

#new registration page
@app.route("/registerNew", methods=['POST'])
def registerPage():
    return render_template("register.html")

#loggin in
@app.route("/auth", methods=['POST'])
def loginCheck():
    hashObj = hashlib.sha1()
    usr = request.form["usr"]
    hashObj.update(request.form["pw"])
    pw = hashObj.hexdigest()
    #if username and password match
    if usr in data:
        if data[usr] == pw:
            return "<center>Login Success!</center>"
        else:
            #otherwise, there is no link between the username and password
            return "<center>Incorrect password!</center>"
        #the username doesnt already exist
    else:
        return "<center>User name doesn't exist!</center>"

#read into the cs file
#I HAVE AN ERROR HERE IN LINE 77
def readFile():
    #open the file in readable
    with open('data.csv','r') as csvfile:
        dataReader = csv.reader(csvfile)
        #for each row
        for row in dataReader:
            if row[0] != "usr" and row[1] != "pw" and (row[0] not in data) :
                data[row[0]] = row[1]

#write to the csv file
def writeFile(u,p):
    #open the file in writable
    with open('data.csv','w') as csvfile:
        dataWriter = csv.writer(csvfile)
        dataWriter.writerow([u,p])

#debugging
if __name__ == "__main__":
    app.debug = True
    app.run()

