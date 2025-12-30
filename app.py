from flask import Flask,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.secret_key="mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db=SQLAlchemy(app)


class Todo(db.Model):
   sno=db.Column(db.Integer , primary_key=True)
   title=db.Column(db.String(300), nullable=False)
   desc=db.Column(db.String(300), nullable=False)
   date_created=db.Column(db.DateTime, default=datetime.utcnow)
# below code must run after table   
with app.app_context():
   db.create_all()

@app.route("/",methods=["GET","POST"])
def hello_world():
   if request.method=="POST":      
      title=request.form["title"]
      desc=request.form["desc"]
      todo=Todo(title=title,desc=desc)
      db.session.add(todo)
      db.session.commit()
      flash("Todo added succesfully","success")
   mytodo=Todo.query.all()
   return render_template("index.html",mytodo=mytodo)

@app.route("/Delete/<int:sno>")
def Delete(sno):
      user=Todo.query.filter_by(sno=sno).first()
      db.session.delete(user)
      db.session.commit()
      flash("Todo deleted succesfully","danger")
      return redirect("/")

@app.route("/Update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
      title=request.form["title"]
      desc=request.form["desc"]
      user=Todo.query.filter_by(sno=sno).first()
      user.title=title
      user.desc=desc
      db.session.add(user)
      db.session.commit()
      flash("Todo updated succesfully","success")
      return redirect("/")
    user=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",user=user)
    


if __name__=="__main__":
   app.run(debug=True,port=8000)