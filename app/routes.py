from app import app
from flask import render_template, redirect, url_for,flash
from app.models import Course, User
from app.forms import ApplyForm, LoginForm
from app import db
from flask_login import login_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/program')
def program_page():
    courses = Course.query.all()
    return render_template('program.html', courses=courses)

@app.route('/apply', methods=['GET', 'POST'])
def apply_page():
    form = ApplyForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              street=form.street.data,
                              city=form.city.data,
                              lga=form.lga.data,
                              state=form.state.data,
                              country=form.country.data,
                              qualification=form.qualification.data,
                              subject_area=form.subject_area.data,
                              username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data,
                              program_apply=form.program_apply.data,
                              start_date=form.start_date.data,
                              )
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('after_apply_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('apply.html', form=form)

@app.route("/after_apply")
@login_required
def after_apply_page():
    return render_template('after_apply.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('after_apply_page'))
        else:
            flash('Usename and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
