import json
import db

from flask import Flask, request
app = Flask(__name__)

Db = db.DB()

@app.route("/")
def hello():
  return "Hello World!"

# ADD MORE ROUTES :)
@app.route('/api/posts/')
def get_posts():
  res = {'success':True, 'data': Db.get_all_posts()}
  return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
  post_body = json.loads(request.data)
  text = post_body['text']
  username = post_body['username']
  post = {
    'id': Db.insert_post_table(text, username),
    'score': 0,
    'text': text,
    'username': username
  }
  return json.dumps({'success': True, 'data': post}), 201

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
  post = Db.get_post_by_id(post_id)
  if post is not None:
    return json.dumps({'success':True, 'data': post}), 200
  return json.dumps({'success': False, 'error': 'Post not fouund'}),404

@app.route('/api/post/<int:post_id>/', methods=['POST'])
def update_post(post_id):
  post_body = json.loads(request.data)
  text = post_body['text']
  Db.update_post_by_id(post_id, text)
  
  post = Db.get_post_by_id(post_id)
  if post is not None:  
    return json.dumps({'success': True, 'data': post})
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
  post = Db.get_post_by_id(post_id)
  if post is not None:
    Db.delete_post_by_id(post_id)
    return json.dumps({'success': True, 'data': post}), 200
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
  post = Db.get_post_by_id(post_id)
  if post is not None:
    comment_list = Db.get_comments_by_post_id(post_id)
    return json.dumps({'success': True, 'data': comment_list}), 200
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/comment/', methods=['POST'])
def post_comment(post_id):
  post = Db.get_post_by_id(post_id)
  if post is not None:
    comment_body = json.loads(request.data)
    text = comment_body['text']
    username = comment_body['username']
    comment = {
        'id': Db.insert_comment_table(post_id, text, username),
        'score': 0,
        'text': text,
        'username': username
    } 
    return json.dumps({'success': True, 'data': comment}), 201
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

# For debugging purposes
@app.route('/api/posts/comments/')
def get_all_comments():
  comments = Db.get_comments()
  return json.dumps({'success': True, 'data': comments}), 201

@app.route('/api/tables/', methods=['DELETE'])
def delete_tables():
    Db.delete_post_table()
    Db.delete_comment_table()
    return json.dumps({'success': True}), 201

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)

