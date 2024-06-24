from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# initialize the app with the extension
db.init_app(app)


class Todo(db.Model):
    sno=db.Column(db.Integer ,primary_key=True)
    title=db.Column(db.String(200) ,nullable=False)
    desc=db.Column(db.String(500) ,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"
    
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world(): 
    
    allTodo = Todo.query.all()   
    return render_template('index.html', todos=allTodo)
    # return 'Hello, World!'

@app.route('/update/<int:sno>',methods=['POST'])
def update(sno):
    todo=Todo.query.filter_by(sno=sno).first()    
    if request.method=='POST':       
      title = request.form.get('title')
      desc = request.form.get('desc')    
     
      todo.title = title
      todo.desc = desc
      db.session.commit()

      return redirect("/")
   
    

@app.route('/delete/<int:sno>')
def delete(sno): 
    
    todo= Todo.query.filter_by(sno=sno).first()  
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
   

@app.route('/add_todo', methods=['POST'])
def add():
    allTodo = Todo.query.all()   
    title = request.form.get('title')
    desc = request.form.get('desc')
    # Create a new TODO object
    todo = Todo(title=title, desc=desc)
   
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))
   
@app.route('/update/<int:sno>')
def products(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)  # Assuming update.html exists


if __name__=="__main__":
    app.run(debug=True ,port=8000)
