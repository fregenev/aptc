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
        if form.program_apply.data == 'Python':
            return redirect(url_for('python_page'))
        elif form.program_apply.data == 'DE':
            return redirect(url_for('data_engineering_page'))
        elif form.program_apply.data == 'WD':
            return redirect(url_for('web_design_page'))
        elif form.program_apply.data == 'WA':
            return redirect(url_for('web_application_page'))
        else:
            return redirect(url_for('machine_learning_page'))    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('apply.html', form=form)

@app.route("/python")
@login_required
def python_page():
    return render_template('python.html')

@app.route("/data_engineering")
@login_required
def data_engineering_page():
    return render_template('data_engineering.html')

@app.route("/web_design")
@login_required
def web_design_page():
    return render_template('web_design.html')

@app.route("/web_application")
@login_required
def web_application_page():
    return render_template('web_application.html')

@app.route("/machine_learning")
@login_required
def machine_learning_page():
    return render_template('machine_learning.html')

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
            if attempted_user.program_apply == 'Python':
                return redirect(url_for('python_page'))
            elif attempted_user.program_apply == 'DE':
                return redirect(url_for('data_engineering_page'))
            elif attempted_user.program_apply == 'WD':
                return redirect(url_for('web_design_page'))
            elif attempted_user.program_apply == 'WA':
                return redirect(url_for('web_application_page'))
            else:
                return redirect(url_for('machine_learning_page'))
        else:
            flash('Usename and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))
