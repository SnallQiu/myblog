# -- coding: utf-8 --
# author: snall  time: 2018/5/1
from .articles import Articles
#from app import db
from . import blog
from .forms import Blog_items
from flask import request,flash,url_for,redirect,render_template
from flask_login import current_user,login_required
import redis
from ..models import User,Post
from .. import db
import time
conn= redis.Redis('127.0.0.1',6379)


@login_required
@blog.route('/<int:page>',methods = ['GET','POST'])
def show_blogs(page):
    form = Blog_items()
    if request.method == 'GET':
        all_blogs = Articles.get_articles(conn,page)
        #print(all_blogs)
        return render_template('blog/show_blogs.html',form=form,blogs=all_blogs)

    else:
        if form.validate_on_submit():
            article_link= str(current_user.id)+'/'+str(int(time.time()))
            article = Post(body = form.body.data,author_id = current_user.id,title=form.title.data,link=article_link)
            db.session.add(article)
            db.session.commit()
            article_id ='article:'+str(article.id)
            score = time.time()+Articles.get_vote_score(conn,article_id)
            Articles.add_to_redis(conn,article_id,score,form,article_link,article)
            flash('You have update a blog!')
        else:
            flash(form.errors)
        return redirect(url_for('blog.show_blogs',page=1))


@blog.route('/info/<path:link>',methods=['GET','POST'])
@login_required
def show_blog_info(link):

    blog_info = Post.query.filter_by(link=link).first_or_404()
    return render_template('blog/show_blog_body.html',blog=blog_info)


@blog.route('/info/<path:link>/count/<int:count>',methods=['GET','POST'])
@login_required
def votes(link,count):
    if request.method=='GET':
        count +=1
        blog_info = Post.query.filter_by(link=link).first_or_404()
        db.session.remove(blog_info)
        blog_info.vote = count
        db.session.add(blog_info)
        db.session.commit()
        return redirect(url_for('blog.show_blog_info',link=link))
