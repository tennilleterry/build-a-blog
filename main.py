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
    
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

        
    if request.method == 'POST':
        name = request.form['name']
        entry = request.form['entry']
        id_name = request.form['id_name']

        

        
        name_error = ''
        entry_error = ''

        if name == "":
            name_error = 'Please fill in the title'
            name = ''
            
        if entry == "":
            entry_error = 'Please fill in the body'
            entry =''

        
         

        if not name_error and not entry_error:
            new_name = Blog(name, entry)
            db.session.add(new_name)
            db.session.commit()
            
            

            post = new_name.id
         
            return redirect('/blog?id={0}'.format(post)) 
             
        else:
            return render_template('newpost.html', name=name, entry=entry, name_error=name_error, entry_error=entry_error)  

        
        
    return render_template('newpost.html')
    

@app.route('/blog')
def blog_page():
    

    
    
    post = Blog.query.all()
        
    return render_template('blog.html', post=post)   
         

   
@app.route('/singlepost')
def single_post():
    
    
    id_name = request.args.get("id")

    posts = Blog.query.filter_by(id=id_name).all()
        
    return render_template('ind_blog.html', posts=posts)
    

    



 
       
    
if __name__ == '__main__':
    app.run()


