from flask import render_template, url_for, redirect, request
from flask.helpers import flash
from flask_login.utils import login_user, logout_user
from devnode import app, bcrypt, db
from devnode.forms import LoginForm, RequestResetForm, ResetPasswordForm, SignupForm, UpdateAccountForm
from flask_login import current_user, login_user, login_required
from devnode.models import User
# from flask_mail import Message
from trycourier import Courier

client = Courier(auth_token="dk_prod_FAM6GKCBX44SYRGDC1JVPB3E8TB8")



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
         email=form.email.data,
         password=hashed_password,
         confirmed=False)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        login_user(user)
        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for("unconfirmed"))
    return render_template('signup.html', form=form, title='Signup')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.confirmed:
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('index'))
            else :
                return redirect(url_for('unconfirmed'))
        else:
            flash("Login Unsuccessful. Please check email and password", 'danger')
    return render_template('login.html', form=form, title='Login')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('index'))
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


def send_confirmation_email(user):
    token = user.get_token()
    # msg = Message('Confirm Your Email',
    #  sender='noreply@demo.com', recipients=[user.email])

    # msg.body = f'''To Confirm Your account, visit the following link:
    # {url_for('confirm_email', token=token, _external=True)}

    # If you did not make this request then simply ignore this email.
    # '''
    # mail.send(msg)

    client.send(
    event="66ZVXFNNSKM3DCKMRNKT9E61ERB6",
    recipient="1ce9bc75-6700-4417-b939-4eb150c2fbc1",
    brand="XZ042R24EH44ZKQF1AQYSS18VDA9",
    profile={
        "email": user.email,
    },
    data={
        "name": user.username,
        "url": url_for('confirm_email', token=token, _external=True),
    },
    )




@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('index')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')


@app.route('/resend')
@login_required
def resend_confirmation_email():
    token = current_user.get_token()

    client.send(
    event="66ZVXFNNSKM3DCKMRNKT9E61ERB6",
    recipient="1ce9bc75-6700-4417-b939-4eb150c2fbc1",
    brand="XZ042R24EH44ZKQF1AQYSS18VDA9",
    profile={
        "email": current_user.email,
    },
    data={
        "name": current_user.username,
        "url": url_for('confirm_email', token=token, _external=True),
    },
    )
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated :
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('password_reset_request.html', title= 'Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated :
        return redirect(url_for('index'))
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. Now you are able to login', 'success')
        return redirect(url_for('login'))
    return render_template('password_reset_confirm.html', title= 'Reset Password', form=form)

def send_reset_email(user):
    token = user.get_token()
    # msg = Message('Password Reset Request',
    #  sender='noreply@demo.com', recipients=[user.email])

    # msg.body = f'''To reset your password, visit the following link:
    # {url_for('reset_token', token=token, _external=True)}

    # If you did not make this request then simply ignore this email.
    # '''
    # mail.send(msg)


    client.send(
    event="78PBTX41D646JGKZ8MTCM6PXQSVY",
    recipient="7179bf35-4578-4730-9660-bd3b77dd4a35",
    brand="XZ042R24EH44ZKQF1AQYSS18VDA9",
    profile={
        "email": user.email,
    },
    data={
        "name": user.username,
        "url": url_for('reset_token', token=token, _external=True),
    },
    )




@login_required
@app.route('/userProfile', methods=['GET', 'POST'])
def user_profile():
    if current_user.is_authenticated and not current_user.confirmed:
        return redirect(url_for('unconfirmed'))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.about.data
        current_user.designation = form.designation.data
        current_user.branch = form.branch.data
        current_user.year = form.year.data
        current_user.twitter_id = form.twitter_id.data
        current_user.linkedin_id = form.linkedin_id.data
        current_user.github_id = form.github_id.data
        current_user.discord_id = form.discord_id.data

        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('user_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about.data = current_user.about
        form.designation.data = current_user.designation
        if current_user.branch !=None:
            form.branch.data = current_user.branch
        if current_user.year !=None:
            form.year.data = current_user.year
        form.twitter_id.data = current_user.twitter_id
        form.linkedin_id.data = current_user.linkedin_id
        form.github_id.data = current_user.github_id
        form.discord_id.data = current_user.discord_id
    return render_template('userProfile.html', title='Account', form=form)


@app.route('/profiles')
def profiles():
    return render_template('profileSection.html')