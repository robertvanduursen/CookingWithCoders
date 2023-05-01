from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, flash, render_template

from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# app.secret_key =
app.wsgi_app = ProxyFix(app.wsgi_app)
'''
https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask


'''


# http://nginx.org/en/docs/beginners_guide.html



@app.route('/hello/<username>')
def hello(username):
    flash('You were successfully logged in')
    return render_template('hello.html', name=username)

# from app import app
from templates.forms import LoginForm
from flask import render_template, flash, redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

'''
G:\Webserver\nginx-1.19.6>start nginx.exe
G:\Webserver\nginx-1.19.6>tasklist /fi "imagename eq nginx.exe"
G:\Webserver\nginx-1.19.6>nginx -s stop
'''

if __name__ == '__main__':
    app.debug = True
    # https://www.reddit.com/r/flask/comments/60dttp/running_flask_in_local_network/
    app.run(host="192.168.2.6", port=65432)
    # app.run()

# todo: how to catch GETS and POSTs to build a little simple firewall to refuse connections other than ours?
