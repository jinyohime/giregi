# -*- coding: utf-8 -*-
from controller import db
from __init__ import bcrypt

class Base(db.Model):
   __abstract__=True
   id=db.Column(db.Integer,primary_key=True)


class User2(Base):
   __tablename__= 'users2'

   username= db.Column(db.String(), unique=True, nullable=False)
   password= db.Column(db.String(), nullable=False)
   email= db.Column(db.String(), unique=True)


   def __init__(self, username, password, email):
      self.username=username
      self.password=bcrypt.generate_password_hash(password=password)
      self.email=email

   def check_password_hash(self,password):
      if bcrypt.check_password_hash(pw_hash=self.password,password=password):
         return True
      else:
         return False

   def __repr__(self):
      return "<E-mail %s>" % self.email



class Article(Base):
   __tablename__='article'
   by=db.Column(db.String(64))
   url=db.Column(db.String(128))
   title=db.Column(db.String(128))
   score=db.Column(db.Integer)
   def __init__(self,by,url,title,score):
      self.url=url
      self.title=title
      self.score=score
      self.by=by


