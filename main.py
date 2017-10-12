from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi 
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Jordyn31@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(255))

    def __init__(self, name, entry):
        self.name = name
        self.entry = entry
        

@app.route("/")
def index():
    #return render_template('base.html')
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():
    

    name = request.args.get('name')
    entry = request.args.get('entry')

    name_error = ''
    entry_error = ''

    if name == "":
        name_error = 'Have to enter a Title'
        

    if entry == "":
        entry_error = 'Have to enter blog post'
        
    
    

    if request.method == 'POST' and not name_error and not entry_error:
        name = request.form['name']
        entry = request.form['entry']

        new_name =Blog(name=name, entry=entry )
        db.session.add(new_name)
        db.session.commit()

        return redirect('/blog')

    else:
        return render_template('newpost.html', name_error=name_error, entry_error=entry_error)


        
    return render_template('newpost.html', name=name, entry=entry)       
    
        
        

    
    
    

@app.route('/blog', methods=['POST', 'GET'])
def blog_page():


    post = Blog.query.all()
        
        
    return render_template('blog.html', post=post)   
        
    
     
    


if __name__ == '__main__':
    app.run()
