from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi 
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build_a_blog:Jordyn31@localhost:8889/build_a_blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    entry = db.Column(db.String(255))

    def __init__(self, name, entry):
        self.name = name
        self.entry = entry
        

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    name_error = ""
    entry_error = ""

    if request.method == 'POST':
        name = request.form['name']
        entry = request.form['entry']

        if name == "":
            name_error = "Enter title of blog post"
            
        if entry == "":
            entry_error = "Enter blog post"


        if not name_error and not entry_error:
            new_blog = Blog(name, entry)
            db.session.add(new_blog)
            db.session.commit()
            id = new_blog.id
            return redirect('/blog?id={}'.format(id))

    return render_template('newpost.html', name_error=name_error, entry_error=entry_error)

@app.route('/blog', methods=['POST', 'GET'])
def home():
        
    blogs = Blog.query.all()
    

    id = request.args.get("id")
    if id is not None:
        blog = Blog.query.get(str(id))
     

        return render_template('single.html', blog=blog)


    return render_template('blog.html', blogs=blogs)


        


    
if __name__ == '__main__':
    app.run()
