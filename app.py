from datetime import datetime, date, timedelta

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    memo = db.Column(db.String(100))
    quantity = db.Column(db.Integer, default=0)

@app.route('/', methods =['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.purchase).all()
        return render_template('index.html', posts=posts,)
    else:
        purchase = request.form.get('purchase')
        title = request.form.get('title')
        genre = request.form.get('genre')
        detail = request.form.get('detail')
        memo = request.form.get('memo')
        
        purchase = datetime.strptime(purchase, '%Y-%m-%d')
        new_post = Post(purchase=purchase, title=title, genre=genre, detail=detail, memo=memo)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.purchase = datetime.strptime(request.form.get('purchase'), '%Y-%m-%d')
        post.title = request.form.get('title')
        post.genre = request.form.get('genre')
        post.detail = request.form.get('detail')
        post.memo = request.form.get('memo')
        
        db.session.commit()
        return redirect('/')

@app.route('/increment/<int:post_id>')
def increment(post_id):
    post = Post.query.get(post_id)
    if post:
        post.quantity += 1
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/decrement/<int:post_id>')
def decrement(post_id):
    post = Post.query.get(post_id)
    if post:
        post.quantity -= 1
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_quantity/<int:post_id>/<action>')
def update_quantity(post_id, action):
    post = Post.query.get(post_id)
    if post:
        if action == 'increment':
            post.quantity += 1
        elif action == 'decrement':
            post.quantity -= 1
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})



# データベースを作成
# with app.app_context():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True)