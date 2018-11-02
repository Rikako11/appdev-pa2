import json
from db import db, Post, Comment
from flask import Flask, request

db_filename = "todo.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    
@app.route('/')
@app.route('/api/posts/')
def get_posts():
    posts = Post.query.all()
    #Comment.query.delete()
    #Post.query.delete()
    #db.session.commit()
    res = {'success': True, 'data': [post.serialize() for post in posts]} 
    return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
    post_body = json.loads(request.data)

    post = Post(
        text = post_body.get('text'),
        username = post_body.get('username')
    )
    db.session.add(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 201

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first() 
    if post is not None:
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/', methods=['POST'])
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        post_body = json.loads(request.data)
        post.text = post_body.get('text', post.text)
        db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404

@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first() 
    if post is not None:
        db.session.delete(post)
        db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404 

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        comments = [comment.serialize() for comment in post.comments]
        return json.dumps({'success': True, 'data': comments}), 200
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404 

@app.route('/api/post/<int:post_id>/comment/', methods=['POST'])
def create_comment(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        comment_body = json.loads(request.data)
        comment = Comment(
            text=comment_body.get('text'),
            username=comment_body.get('username'),
            post_id=post.id
        )
        post.comments.append(comment)
        db.session.add(comment)
        db.session.commit()
        return json.dumps({'success': True, 'data': comment.serialize()}), 201
    return json.dumps({'success': False, 'error': 'Post not found!'}), 404 

@app.route('/api/post/<int:post_id>/vote/', methods=['POST'])
def update_post_vote(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is not None:
        vote_body = json.loads(request.data)
        vote = vote_body.get('vote')
        if vote == "" or vote:
           post.score += 1
           db.session.commit()
        elif not vote:
           post.score -= 1
           db.session.commit()
        return json.dumps({'success': True, 'data': post.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Post not found or vote is invalid!'}), 404

@app.route('/api/comment/<int:comment_id>/vote/', methods=['POST'])
def update_comment_vote(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is not None:
        vote_body = json.loads(request.data)
        vote = vote_body.get('vote')
        if vote == "" or vote:
           comment.score += 1
           db.session.commit()
        elif not vote:
           comment.score -= 1
           db.session.commit()
        return json.dumps({'success': True, 'data': comment.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Comment not found or vote is invalid!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
