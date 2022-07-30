from flask import Flask,render_template,request,redirect
from models import db,StudentModel
#baru
from flask_mysqldb import MySQL, MySQLdb
from flask import Flask, render_template, session, url_for, redirect, request

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
#baru
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.config["SECRET_KEY"] = "iniSecretKeyKu2019"

#login
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cur.fetchone()
            cur.close()

            if len(user) > 0:
                    session['name'] = user['name']
                    session['email'] = user['email']
                    return render_template("home.html")

            else:
                return "eror"    
    return render_template("index.html")

#baru
@app.before_first_request
def create_table():
    db.create_all()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')
 
    if request.method == 'POST':

        #hobby = request.form.getlist('hobbies')
        #hobbies = ','.join(map(str, hobby))
        #hobbies=",".join(map(str, hobby))


        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email =email,
            password = password

        )
        db.session.add(students)
        db.session.commit()
        return redirect('/news')
 
 
@app.route('/news')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html',students = students)
 
 
@app.route('/<int:id>')
def RetrieveStudent(id):
    students = StudentModel.query.filter_by(id=id).first()
    if students:
        return render_template('data.html', students = students)
    return f"Employee with id ={id} Doenst exist"
 
 
@app.route('/<int:id>/edit',methods = ['GET','POST'])
def update(id):
    student = StudentModel.query.filter_by(id=id).first()

    #hobbies = student.hobbies.split(' ')
    # print(hobbies)
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
    #     tv = request.form['tv']    
    #     if tv is None:
    #               pass

    #    # print('Form:' + str(request.form))    
      
    #     cricket = request.form['cricket']
    #     movies = request.form['movies']
    #     hobbies = tv + ' ' +  cricket + ' ' + movies
    #     print('H' + hobbies)
        #hobby = request.form.getlist('hobbies')
        #hobbies = ','.join(map(str, hobby))
        #hobbies =  ",".join(map(str, hobby)) 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']


        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,

        )
        db.session.add(student)
        db.session.commit()
        return redirect('/news')
        return f"Student with id = {id} Does nit exist"
 
    return render_template('update.html', student = student)
 
 
@app.route('/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    students = StudentModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect('/news')
        abort(404)
     #return redirect('/')
    return render_template('delete.html')

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True, port=5000) 
#app.run(host='localhost', port=5000)