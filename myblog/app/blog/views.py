# -- coding: utf-8 --
# author: snall  time: 2018/5/1
from .articles import Articles
#from app import db
from . import blog
from .forms import Blog_items,Ensure_Delete,Search_keywords,Comment_submit,Comment_info
from flask import request,flash,url_for,redirect,render_template
from flask_login import current_user,login_required
import redis
from ..models import User,Post
from .. import db
import time
from markdown import markdown
conn= redis.Redis('127.0.0.1',6379)
pipeline = conn.pipeline()

@login_required
@blog.route('/<int:page>',methods = ['GET','POST'])
def show_blogs(page):
    blog_form = Blog_items()
    search_form = Search_keywords()
    all_blogs = Articles.get_articles(conn, page)
    if request.method == 'GET':
        #print(all_blogs)
        return render_template('blog/show_blogs.html',form=blog_form,blogs=all_blogs,search_form=search_form)

    else:
        if blog_form.validate_on_submit():
            article_link= str(current_user.username)+'/'+str(int(time.time()))
            article = Post(body = blog_form.body.data,author_id = current_user.id,title=blog_form.title.data,link=article_link)
            db.session.add(article)
            db.session.commit()
            article_id ='article:'+str(article.id)
            score = int(time.time()/10000000)+Articles.get_vote_score(conn,article_id)
            title = blog_form.title.data
            Articles.add_to_redis(conn=conn,article_id=article_id,score=score,article_link=article_link,article=article,title=title)

            flash('You have update a blog!')
        elif search_form.validate_on_submit():
            key_word = search_form.data
            return redirect(url_for('blog.search_keyword',keyword = key_word['search']))
        else:
            flash(blog_form.errors)
        return redirect(url_for('blog.show_blogs',page=1))


@blog.route('/info/<path:link>',methods=['GET','POST'])
@login_required
def show_blog_info(link):
    if request.method == "GET":
        form_del = Ensure_Delete()
        form_edit = Blog_items()
        comment_info = Comment_info()
        blog_info = Post.query.filter_by(link=link).first_or_404()
        form_edit.body.data = blog_info.body
        form_edit.title.data = blog_info.title
        can_edit = False
        #show_comment = Comment.query.filter(id=blog_info.id)#从数据库找
        blog_comment = conn.hgetall('comment:'+str(blog_info.id))
        '''snall:nice blog！'''
        if blog_info.author_id == current_user.id or current_user.username == 'snall':
            can_edit = True
        return render_template('blog/show_blog_body.html',
                               blog=blog_info,
                               can_edit=can_edit,
                               form_del=form_del,
                               comment_info = comment_info,
                               form_edit=form_edit,
                               blog_comment=blog_comment,
                               )

    else:
        comment_info = Comment_info()
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
        if comment_info.validate_on_submit():
            conn.hmset('comment:'+str(blog_info.id),{comment_info.data['comment_info']:current_user.username})
            return redirect(url_for('blog.show_blog_info', link=link))
            '''放进数据库里'''

        





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


@blog.route('/show_myblog/<int:page>',methods=['GET','POST'])
@login_required
def show_my_blogs(page):
    form = Blog_items()
    search_form = Search_keywords()
    if request.method == 'GET':

        all_blogs = Articles.get_articles(conn,page,username=current_user.username)
        #print(all_blogs)
        return render_template('blog/show_blogs.html',form=form,blogs=all_blogs,search_form=search_form)

    else:
        if form.validate_on_submit():
            article_link= str(current_user.username)+'/'+str(int(time.time()))
            article = Post(body = form.body.data,author_id = current_user.id,title=form.title.data,link=article_link)
            db.session.add(article)
            db.session.commit()
            article_id ='article:'+str(article.id)
            score = int(time.time())+Articles.get_vote_score(conn,article_id)
            Articles.add_to_redis(conn,article_id,score,form,article_link,article)
            flash('You have update a blog!')
        else:
            flash(form.errors)
        return redirect(url_for('blog.show_blogs',page=1))


@blog.route('/search/<keyword>',methods=['GET','POST'])
def search_keyword(keyword):
    '''用户搜索记录，如果已经有人搜索过，就缓存下来'''
    search_form = Search_keywords()
    if conn.sismember('search_keywords',keyword):
        find_articles = Articles.get_articles(conn=conn, page=1, keyword=keyword)
        #print(find_articles)
        return render_template('blog/show_blogs.html',blogs=find_articles,search_form=search_form)

    else:
        all_blogs = Post.query.all()
        for blog in all_blogs:
            if keyword in blog.body or keyword in blog.title:
                Articles.add_to_redis(conn,article_id=blog.id,article_link=blog.link,article=blog,keyword = keyword,
                                      title=blog.title,search=True)
        find_articles = Articles.get_articles(conn=conn,page=1,keyword=keyword)

        conn.sadd('search_keywords',keyword)
        return render_template('blog/show_blogs.html',blogs=find_articles,search_form=search_form)




'''
以后在解决图片分栏显示问题---------
 <div class="col-lg-6">
    <img src="https://farm5.staticflickr.com/4290/35294660055_42c02b2316_k_d.jpg" width="568" height="466" style="position: relative;left: 600px">
    </div>
'''