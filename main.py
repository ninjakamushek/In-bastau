import os

from flask import Flask, render_template, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_restful import abort, Api
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from Forms.StartupCreationForm import StartupCreationForm
from LoginForm import LoginForm
from RegisterForm import RegisterForm
from data import db_session
from data.startup import Startup
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'In-bastau-secret-key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', title='In-bastau')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form, message="Пароли не совпадают")
        if len(form.password.data) < 8:
            return render_template('registration.html', title='Регистрация',
                                   form=form, message="Пароль не может быть короче 8 символов")
        if form.password.data.isalpha():
            return render_template('registration.html', title='Регистрация',
                                   form=form, message="Пароль должен содержать хотя бы одну цифру")
        if form.password.data.isdigit():
            return render_template('registration.html', title='Регистрация',
                                   form=form, message="Пароль должен содержать хотя бы одну букву")
        if form.password.data.isalnum():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароль должен содержать хотя бы один символ отличный от "
                                           "букв и цифр")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form, message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create_startup', methods=['GET', 'POST'])
def create_startup():
    form = StartupCreationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        startup = Startup()
        startup.name = form.name.data
        startup.description = form.description.data
        startup.author_id = current_user.id
        session.add(startup)
        session.commit()
    return render_template('creating_startup.html', title='Создание стартапа', form=form)


def run_local():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="127.0.0.1", port=port)


def main():
    db_session.global_init("db/In-bastau.sqlite")
    run_local()


if __name__ == '__main__':
    main()
