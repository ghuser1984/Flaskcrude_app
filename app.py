from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class ToDolist(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task {}>'.format(self.id)


 
@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        if len(task_content)==0:
            return render_template('empty_task.html')  
        else:
            new_task=ToDolist(content=task_content)
        try:
            db.session.add(new_task) #adding new task
            db.session.commit()      #updating database   
            return redirect('/')     #getting back to start page
        except:
            return render_template('error.html')
    
    else:
        tasks=ToDolist.query.order_by(ToDolist.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')      #shown in the left lower corner of browser window when howerin over the link
def delete(id): #deleting task by it's unique id 
    task_to_delete=ToDolist.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return render_template('error.html')

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task=ToDolist.query.get_or_404(id)
    if request.method=="POST":
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return render_template('error.html')
    else:
        return render_template('update.html',task=task)

    


if __name__=="__main__":
    app.run(debug=True)