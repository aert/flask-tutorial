from flask import Blueprint, flash, redirect, url_for, render_template, g
from flask.ext.login import login_required
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Length
from microblog.extensions import db
from microblog.models import User


user_bp = Blueprint('user', __name__)


# --- Forms -------------------------------------------------------------------

class EditForm(Form):
    nickname = TextField('nickname', validators=[Required()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])


# --- Controllers -------------------------------------------------------------

@user_bp.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index.home'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
    ]
    return render_template('frontend/user.html',
                           title='User',
                           user=user,
                           posts=posts)


@user_bp.route("/user/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('frontend/user_edit.html',
                               title="User Edit",
                               form=form)
