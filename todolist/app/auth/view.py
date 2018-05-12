# -- coding: utf-8 --
# author: snall  time: 2018/4/22
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from .form import Register_User_Form,LoginForm
from . import auth
from app import login_manager
from ..models import User
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user)
            flash('you have logged in!')
            return redirect(url_for('main.show_todo_list',name=user.username))
        else:
            flash('Invalid username or password')
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@auth.route('/register',methods=['GET','POST'])
def register():
    form = Register_User_Form()
    if form.validate_on_submit():
        user = User(#id = 1,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)
