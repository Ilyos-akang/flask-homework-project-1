from flask import Flask,render_template,url_for,redirect,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.orm import relationship
import os

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.secret_key="nimadur"

app.config["UPLOAD_FOLDER"]="static/rasmlar"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
os.makedirs(app.config["UPLOAD_FOLDER"],exist_ok=True)
ALLOWED_EXTENSIONS=['png','jpg','jpeg','gif']

db=SQLAlchemy(app)



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ism = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    parol = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    talabalar=db.relationship("Talaba",backref="user",lazy=True)
    
    def __repr__(self):
        return f"User: {self.ism}"

class Talaba(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    t_yil=db.Column(db.Integer,default=2007)
    ismi=db.Column(db.String(100),)
    fakultet=db.Column(db.String(200),default="")
    yunalish=db.Column(db.String(100),default="")
    kurs=db.Column(db.Integer,default=1)
    phone_number=db.Column(db.String(200),default="")
    image_url=db.Column(db.String(200),default="static/rasmlar/default.png")

    def __repr__(self):
        return f"Talaba: {self.ismi} | tug'ilgan yili {self.t_yil}"



@app.route("/")
def index():
    ism=session.get("ism")
    if ism is None:
        return redirect (url_for('login'))
    talaba=Talaba.query.all()
    user_id=session.get("user_id")
    return render_template ('index.html',ism=ism,talaba=talaba,user_id=user_id)



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        phone_number=request.form.get("phone")
        parol=request.form.get("parol")
        user=Users.query.filter_by(
            phone_number=phone_number,
            parol=parol

        ).first()
        if user:
            session['ism']=user.ism
            session['user_id']=user.id
            return redirect (url_for('index'))
        return redirect (url_for('login'))
    

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        ism=request.form.get("ism")
        phone_number=request.form.get('phone')
        parol=request.form.get('parol')
        try:
            user=Users(
                ism=ism,
                phone_number=phone_number,
                parol=parol
            )
            db.session.add(user)
            db.session.commit()
            session['ism']=user.ism
            session['user_id']=user.id
            return redirect(url_for('index'))
        except:
            return redirect(url_for('register'))



if __name__=="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)