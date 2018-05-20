# -- coding: utf-8 --
# author: snall  time: 2018/5/1
from .articles import Articles
#from app import db
from . import blog
from .forms import Blog_items,Ensure_Delete
from flask import request,flash,url_for,redirect,render_template
from flask_login import current_user,login_required
import redis
from ..models import User,Post
from .. import db
import time
from markdown import markdown
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
            article_link= str(current_user.username)+'/'+str(int(time.time()))
            article = Post(body = form.body.data,author_id = current_user.id,title=form.title.data,link=article_link)
            db.session.add(article)
            db.session.commit()
            article_id ='article:'+str(article.id)
            score = int(time.time()/10000000)+Articles.get_vote_score(conn,article_id)
            Articles.add_to_redis(conn,article_id,score,form,article_link,article)
            flash('You have update a blog!')
        else:
            flash(form.errors)
        return redirect(url_for('blog.show_blogs',page=1))


@blog.route('/info/<path:link>',methods=['GET','POST'])
@login_required
def show_blog_info(link):
    if request.method == "GET":
        form_del = Ensure_Delete()
        form_edit = Blog_items()
        blog_info = Post.query.filter_by(link=link).first_or_404()
        form_edit.body.data = blog_info.body
        form_edit.title.data = blog_info.title
        can_edit = False
        if blog_info.author_id == current_user.id:
            can_edit = True
        return render_template('blog/show_blog_body.html', blog=blog_info, can_edit=can_edit, form_del=form_del,
                               form_edit=form_edit)

    else:
        form_edit = Blog_items()
        form_del = Ensure_Delete()
        blog_info = Post.query.filter_by(link=link).first_or_404()

        if form_del.status.data == '1':
            return redirect(url_for('blog.delete_blog', id=blog_info.id))
        if form_edit.validate_on_submit():
            '''这里没有修改 from_edit没有修改'''
            blog_info.title = form_edit.title.data
            blog_info.body = form_edit.body.data
            db.session.commit()
            '''modify redis '''
            conn.hset('article:'+str(blog_info.id),'title',blog_info.title)
            flash('Your have modifyed a blog!')
            return redirect(url_for('blog.show_blog_info', link=link))
        





@blog.route('/info/<path:link>/count/<int:count>',methods=['GET','POST'])
@login_required
def votes(link,count):
    if request.method=='GET':
        blog_info = Post.query.filter_by(link=link).first_or_404()
        voted_key = 'voted:'+str(blog_info.id)
        voted_user = 'user:'+str(current_user.id)
        score_key = 'article:'+str(blog_info.id)
        if not conn.sismember(voted_key,voted_user):
            count += 1
            blog_info.vote = count
            db.session.commit()
            conn.sadd(voted_key,voted_user)           #将点过赞的用户添加到'voted:(article_id)'
            conn.zincrby('score:',score_key,10)       #增加文章评分
        else:
            flash('you have voted!')
        return redirect(url_for('blog.show_blog_info', link=link))


@blog.route('/delete/<int:id>')
@login_required
def delete_blog(id):
    blog_info = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(blog_info)
    db.session.commit()
    Articles.delete_blog(conn,id)
    flash('You have delete a blog')
    return redirect(url_for('blog.show_blogs',page=1))
