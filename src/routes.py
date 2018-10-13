import json

from flask import Flask, request
app = Flask(__name__)

post_id_counter = 2

comment_id_counter = [1, 0]

posts = {
  0: {
    'id': 0,
    'score': 0,
    'text': 'My First Post!',
    'username': 'Young',
  },
  1: {
    'id': 1,
    'score': 0,
    'text': 'My Second Post!',
    'username': 'Young'
  }
}

comments = {
  0: [
      { 
        'id': 0,
        'score': 0,
        'text': 'My First Comment!',
        'username': 'Young'
      }
  ],
  1:[]
}   

@app.route("/")
def hello():
  return "Hello World!"

# ADD MORE ROUTES :)
@app.route('/api/posts/')
def get_posts():
  res = {'success':True, 'data': list(posts.values())}
  return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
  global post_id_counter
  post_body = json.loads(request.data)
  score = 0
  text = post_body['text']
  username = post_body['username']
  post = {
    'id': post_id_counter,
    'score': score,
    'text': text,
    'username': username
  }
  posts[post_id_counter] = post
  comment_id_counter.append(0)
  comments[post_id_counter] = []
  post_id_counter += 1
  return json.dumps({'success': True, 'data': post}), 201

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
  if post_id in posts:
    post = posts[post_id]
    return json.dumps({'success':True, 'data': post}), 200
  return json.dumps({'success': False, 'error': 'Post not fouund'}),404

@app.route('/api/post/<int:post_id>/', methods=['POST'])
def update_post(post_id):
  if post_id in posts:
    post = posts[post_id]
    post_body = json.loads(request.data)
    post['text'] = post_body['text']
    return json.dumps({'success': True})
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
  if post_id in posts:
    post = posts[post_id]
    del posts[post_id]
    return json.dumps({'success': True, 'data': post}), 200
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
  if post_id in posts:
    comment_list = comments[post_id]
    return json.dumps({'success': True, 'data': comment_list}), 200
  return json.dumps({'success': False, 'error': 'Post not found'}), 404

@app.route('/api/post/<int:post_id>/comment/', methods=['POST'])
def post_comment(post_id):
  if post_id in posts:
    global comment_id_counter
    post_body = json.loads(request.data)
    comment_id = comment_id_counter[post_id]
    comment = {
      'id': comment_id,
      'score': 0,
      'text': post_body['text'],
      'username': post_body['username']
    }
    comments[post_id].append(comment)
    comment_id_counter[post_id] += 1
    return json.dumps({'success': True, 'data': comment}), 201
  return json.dumps({'success': False, 'error': 'Post not found'}), 404
    
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
