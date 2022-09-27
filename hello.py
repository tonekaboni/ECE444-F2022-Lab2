
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class infoForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your Uoft Email Address?', validators=[DataRequired(),Email('please enter a valid email containing @')])
    submit = SubmitField('Submit')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = infoForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        email_in = form.email.data
        old_email = session.get('email')
        if old_email is not None and old_email != email_in:
            flash('Looks like you have changed your email!')
        if 'utoronto.ca' in email_in:
            session['email'] = email_in
        else:
            #please keep in mind that invalid cannot be the address itself as the email validator will catch it
            session['email'] = 'invalid'
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),email=session.get('email'))
