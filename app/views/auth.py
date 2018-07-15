from flask_classful import FlaskView, route
from flask import render_template, request, flash, session, redirect, url_for
from app.models.user import User
from app.models.account import Account


class Auth(FlaskView):
    trailing_slash = False
    route_base = ''

    @route('/login', methods=['GET'])
    def index(self):
        return self._render('auth/login.html', 'Login')

    @route('/login', methods=['POST'])
    def post(self):
        if len(request.form['username']) == 0 or len(request.form['password']) == 0:
            flash('Both username & password are required', 'error')
            return self._render('auth/login.html', 'Login')
        user = User.query.filter_by(audit_is_deleted=False, username=request.form['username']).first()
        if not user or not user.validate_password(request.form['password']):
            flash('Username or password incorrect', 'error')
            return self._render('auth/login.html', 'Login')
        session['user_id'] = user.id
        return redirect(url_for('Dashboard:index'))

    @route('/signup', methods=['GET'])
    def signup(self):
        return self._render('auth/signup.html', 'Register')

    @route('/signup', methods=['POST'])
    def signup_post(self):
        if Account.query.filter_by(audit_is_deleted=False, name=request.form['account_name']).first():
            flash('Account name already in use', 'error')
            return self._render('auth/signup.html', 'Register')
        if User.query.filter_by(audit_is_deleted=False, username=request.form['username']).first():
            flash('Username already in use', 'error')
            return self._render('auth/signup.html', 'Register')
        if User.query.filter_by(audit_is_deleted=False, email_address=request.form['email_address']).first():
            flash('Email address already in use', 'error')
            return self._render('auth/signup.html', 'Register')
        if request.form['password'] != request.form['password_confirm']:
            flash('Password and confirmation do not match', 'error')
            return self._render('auth/signup.html', 'Register')

        account = Account(name=request.form['account_name'])
        account.create()

        user = User(username=request.form['username'],
                    email_address=request.form['email_address'],
                    account_id=account.id)
        user.create()

        user.update_password(request.form['password'])

        flash('User created successfully, Please login', 'success')
        return self._render('auth/login.html', 'Login')

    @staticmethod
    def _render(template, page_title):
        return render_template(template, page_title=page_title, req=request.form)
