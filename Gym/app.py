
from flask import Flask, render_template, request, session,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="C:\oracle\instantclient_21_10")

app = Flask(__name__)
app.secret_key="HeyWhatsUp!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'
db=SQLAlchemy(app)






class Gymmanagement(db.Model):

    username = db.Column(db.String(20),unique=True ,nullable=False ,primary_key = True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    joindate = db.Column(db.String(20))
    mobile = db.Column(db.Integer)
    slot = db.Column(db.String(20))
    paymentstatus = db.Column(db.String(20))





#home page
@app.route("/")
def home():
    return render_template("index.html")

# go to admin login page
@app.route("/admin")
def loginpage():
    return render_template('adminlogin.html')

#go to admin login page
@app.route("/index1")
def index1():
    return render_template('adminlogin.html')


#admin login session username password
@app.route("/adminlogin", methods = ['POST','GET'])
def adminlogin():
    if request.method == 'POST':
        adminuser = request.form.get('adminusername')
        adminpass = request.form.get('adminpass')

        if(adminuser=="Niraj" and adminpass=="Niraj@123"):
            session['usern'] = adminuser
            return render_template('sucess.html')
        else:
            msg = "Invalid Credentials"
            return render_template('adminlogin.html', msg=msg)
    return render_template('adminlogin.html')


# Admin logout
@app.route('/logout')
def logout():
    session.pop('usern', None)
    session.clear()
    return redirect(url_for('index1'))


# way to logout page
@app.route('/waytologout')
def waytologout():
    return render_template('/logout.html')

# ADMIN : select all registration details
@app.route("/showdetails")
def showdetails():
    alldetails = Gymmanagement.query.all()
    return render_template("adminregdet.html", alldetails=alldetails)


#ADMIN: Delete registration detail
@app.route('/delete/<username>')
def delete(username):
    detail = Gymmanagement.query.filter_by(username=username).first()
    db.session.delete(detail)
    db.session.commit()
    return redirect('/showdetails')

#Admin update: user detail update
@app.route('/update/<username>' ,methods=['GET','POST'])
def update(username):
    entry=Gymmanagement.query.get(username)
    if request.method=='POST':
        entry.username=request.form.get('username')
        entry.password=request.form.get('password')
        entry.name=request.form.get('name')
        entry.surname=request.form.get('surname')
        entry.age=request.form.get('age')
        entry.weight=request.form.get('weight')
        entry.mobile=request.form.get('mobile')
        entry.joindate=request.form.get('joindate')
        entry.slot=request.form.get('slot')
        entry.paymentstatus=request.form.get('paymentstatus')

        db.session.add(entry)
        db.session.commit()
        return redirect("/showdetails")

    return render_template('update.html',entry=entry)



# user detail display
@app.route("/user", methods=['POST','GET'])
def show():
    userinfo = Gymmanagement.query.filter_by(username=session.get('user')).first_or_404()
    username = userinfo.username
    entries=Gymmanagement.query.filter_by(username=username)
    return render_template('user.html',entries=entries)



# User login
@app.route("/login" , methods=['GET' ,'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:

            insert = Gymmanagement.query.filter_by(username=username).first_or_404()

        except:
            msg1 = "Invalid Credentials"
            return render_template('index.html', msg1=msg1)

        if password == insert.password:

            session["user"] = username
            return render_template("/user.html")
        else:

            msg = "Invalid Credentials"
            return render_template('index.html', msg=msg)

    return render_template("/user.html")


#User Logout
@app.route('/dropsession', methods=['GET','POST'])
def dropsession():
    session.pop('username',None)
    session.clear()
    return render_template('index.html')



# User Registration


@app.route("/register" ,methods=['POST','GET'])
def insert():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        username=request.form.get('username')
        password=request.form.get('password')
        name=request.form.get('name')
        surname=request.form.get('surname')
        age=request.form.get('age')
        weight = request.form.get('weight')
        mobile = request.form.get('mobile')
        joindate = request.form.get('joindate')
        slot=request.form.get('slot')
        paymentstatus= request.form.get('paymentstatus')


        entry = Gymmanagement(username=username, password=password,name=name,surname=surname,age=age,weight=weight,mobile=mobile,joindate=joindate, slot=slot,paymentstatus=paymentstatus)

        db.create_all() #for creating table
        db.session.add(entry)
        db.session.commit()

    else:
        return  render_template('register.html')

    return render_template('index.html')



# return admin login to user login
@app.route("/main")
def returnlogin():
    return render_template("/index.html")

if __name__ == "__main__":
    app.run(debug=True)

