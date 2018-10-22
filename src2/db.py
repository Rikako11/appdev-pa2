import os
import json
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class DB(object):
    """
    DB driver for the Todo app - deals with writing entities
    to the DB and reading entities from the DB
    """

    def __init__(self):
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.create_post_table()
        self.create_comment_table()

    def create_post_table(self):
        try:
            self.conn.execute("""
                CREATE TABLE post (
                    ID INTEGER PRIMARY KEY,
                    SCORE INTEGER,
                    TEXT TEXT NOT NULL,
                    USERNAME TEXT NOT NULL
                );
            """)
        except Exception as e:
            print(e)
    
    def create_comment_table(self):
        try:
           self.conn.execute("""
               CREATE TABLE comments (
                   ID INTEGER PRIMARY KEY,
                   POST_ID INTEGER,
                   SCORE INTEGER,
                   TEXT TEXT NOT NULL,
                   USERNAME TEXT NOT NULL
               );
           """)
        except Exception as e:
           print(e)

    def delete_post_table(self):
        self.conn.execute('DROP TABLE IF EXISTS post;')

    def delete_comment_table(self):
        self.conn.execute('DROP TABLE IF EXISTS comments;')

    def get_all_posts(self):
        cursor = self.conn.execute('SELECT * FROM post;')
        posts = []

        for row in cursor:
            posts.append({'id': row[0], 'score': row[1], 'text': row[2], 'username':row[3]})

        return posts

    def insert_post_table(self, text, username):
        cur = self.conn.cursor()
        cur.execute('INSERT INTO post (SCORE, TEXT, USERNAME) VALUES (?, ?, ?);', 
            (0, text, username))
        self.conn.commit()
        return cur.lastrowid

    def get_post_by_id(self, id):
        cursor = self.conn.execute('SELECT * FROM post WHERE ID == ?', (id,))

        for row in cursor:
            return {'id': row[0], 'score': row[1], 'text': row[2], 'username':row[3]}

        return None

    def update_post_by_id(self, id, text):
        self.conn.execute("""
            UPDATE post 
            SET TEXT = ?
            WHERE ID = ?;
        """, (text, id))
        self.conn.commit()

    def delete_post_by_id(self, id):
        self.conn.execute("DELETE FROM post WHERE ID == ?;", (id,))
        self.conn.commit()
     
    def insert_comment_table(self, post_id, text, username):
        cur = self.conn.cursor()
        cur.execute("""
             INSERT INTO comments (POST_ID, SCORE, TEXT, USERNAME)
             VALUES(?, ?, ?, ?);
        """, (post_id, 0, text, username,))
        self.conn.commit()
        return cur.lastrowid

    def get_comments_by_post_id(self, post_id):
        cur = self.conn.execute("""
            SELECT * FROM comments WHERE POST_ID == ?
        """, (post_id,))
        comments = []

        for row in cur:
            comments.append({'id': row[0], 'score': row[2], 'text': row[3], 'username': row[4] })
        
        return comments
 
    def get_comments(self):
        cur = self.conn.execute("SELECT * FROM comments")
        comments = [] 
        for row in cur:
            comments.append({'id': row[0], 'score': row[2], 'text': row[3], 'username': row[4]})
        return comments
