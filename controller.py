# -*- coding: utf-8 -*-
from flask import request, render_template, session, redirect, url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import timedelta

from __init__ import app

db= SQLAlchemy(app)
	
from models import *


@app.route('/')
def index():
	article_query=Article.query.order_by(Article.score).all()
	article_query.reverse()
	return render_template('index.html',articles=article_query)	





	
@app.route('/logout')
def logout():
	session['logged_in']=False
	session.pop('username',None)
	return redirect(url_for('index'))

@app.route('/login')
def login():
	if 'logged_in' in session:
		if session['logged_in']:
			return redirect(url_for('index'))
		else:
			return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/login/check', methods=['POST'])
def login_check():
	username=request.form['username']
	pw=request.form['password']
	user_query=User2.query.filter(User2.username==username).first()
	if user_query:
		if user_query.check_password_hash(pw):
			session['logged_in']=True
			session['username']=username
			return redirect(url_for('index'))
		else:
			return 'password wrong'
	else:
		return 'id wrong'

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/signup/check',methods=['POST'])
def signup_check():
	username=request.form['username']
	password=request.form['password']
	email=request.form['email']
	user2=User2(username,password,email)
	db.session.add(user2)
	db.session.commit()
	return redirect(url_for('index'))



@app.before_request
def make_session_timeout():
	session.permanent=True
	app.permanent_session_lifetime=timedelta(minutes=5)

@app.route('/write_post')
def write_post_page():
	if 'logged_in' in session:
		if session['logged_in']:
			return render_template('write_post.html')
	return redirect(url_for('login'))

@app.route('/write_check',methods=['POST'])
def write_check():
	post_title=request.form['post_title']
	post_body=request.form['post_body']
	user_query=User2.query.filter(User2.username==session['username']).first()
	p=Post2(user_query.id,post_title,post_body)
	db.session.add(p)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/add_article',methods=['POST'])
def add_article():
	url=request.form['url']
	title=request.form['title']
	by=request.form['by']
	k=Article(by,url,title,0)
	db.session.add(k)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/add_article_page')
def add_article_page():
	return render_template('add_article.html')

@app.route('/like/<temp>',methods=['GET'])
def like(temp):
	a=Article.query.filter(Article.title==temp).first()
	a.score+=1
	db.session.add(a)
	db.session.commit()
	return redirect(url_for('index'))


@app.route('/delete/<temp>',methods=['GET'])
def delete(temp):
	a=Article.query.filter(Article.title==temp).first()
	db.session.delete(a)
	db.session.commit()
	return redirect(url_for('index'))