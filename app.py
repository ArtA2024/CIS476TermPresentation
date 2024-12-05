from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegistrationForm, LoginForm
from models import db, User, VaultItem, Notification
from utils import generate_password
from recovery_chain import Question1Step, Question2Step, Question3Step
from mediators import DashboardMediator
from components import VaultView, VaultForm
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Initialize mediator and components
mediator = DashboardMediator()
vault_view = VaultView(mediator)
vault_form = VaultForm(mediator)

# Register components with the mediator
mediator.register("vault_view", vault_view)
mediator.register("vault_form", vault_form)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return redirect(url_for('login'))

#Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.master_password.data)
        user = User(
            email=form.email.data,
            master_password=hashed_password,
            security_q1=form.security_q1.data,
            security_a1=form.security_q1_answer.data,
            security_q2=form.security_q2.data,
            security_a2=form.security_q2_answer.data,
            security_q3=form.security_q3.data,
            security_a3=form.security_q3_answer.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.master_password, form.master_password.data):
            session['user_id'] = user.id
            flash('Master password verified. Please answer your security questions.', 'info')
            return redirect(url_for('verify_questions'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/generate_password', methods=['GET'])
def generate_password_api():
    """API route to generate a password."""
    length = request.args.get('length', default=12, type=int)
    include_special = request.args.get('include_special', default=True, type=bool)
    try:
        password = generate_password(length, include_special)
        return jsonify({"password": password})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

#Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    vault_items = VaultItem.query.filter_by(user_id=user_id).all()
    notifications = Notification.query.filter_by(user_id=user_id, read=False).all()
    return render_template('dashboard.html', vault_items=vault_items, notifications=notifications)

#Add Item route
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_data = {
            "title": request.form.get('title'),
            "item_type": request.form.get('item_type'),
            "username": request.form.get('username'),
            "password": request.form.get('password'),
            "credit_card_number": request.form.get('credit_card_number'),
            "cvv": request.form.get('cvv'),
            "secure_note": request.form.get('secure_note'),
            "url": request.form.get('url'),
            "full_name": request.form.get('full_name'),
            "address": request.form.get('address'),
            "phone_number": request.form.get('phone_number'),
            "passport_number": request.form.get('passport_number'),
            "passport_expiration": request.form.get('passport_expiration'),
            "driver_license": request.form.get('driver_license'),
            "license_expiration": request.form.get('license_expiration'),
            "ssn": request.form.get('ssn'),
            "credit_card_expiration": request.form.get('credit_card_expiration'),
            "user_id": session['user_id'],
        }
        vault_item = VaultItem(**item_data)
        db.session.add(vault_item)
        db.session.commit()

        # Trigger observer-style checks
        vault_item.notify_observers()

        flash('Item added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_item.html')

#Edit Item route
@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    item = VaultItem.query.get_or_404(item_id)

    if request.method == 'POST':
        item.title = request.form.get('title')
        item.username = request.form.get('username')
        item.password = request.form.get('password')
        item.credit_card_number = request.form.get('credit_card_number')
        item.cvv = request.form.get('cvv')
        item.secure_note = request.form.get('secure_note')
        item.url = request.form.get('url')
        item.full_name = request.form.get('full_name')
        item.address = request.form.get('address')
        item.phone_number = request.form.get('phone_number')
        item.passport_number = request.form.get('passport_number')
        item.passport_expiration = request.form.get('passport_expiration')
        item.driver_license = request.form.get('driver_license')
        item.license_expiration = request.form.get('license_expiration')
        item.ssn = request.form.get('ssn')
        item.credit_card_expiration = request.form.get('credit_card_expiration')

        db.session.commit()

        # Trigger observer-style checks
        item.notify_observers()

        flash('Item updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_item.html', item=item)

#Toggle Mask route
@app.route('/toggle_mask/<int:item_id>', methods=['POST'])
def toggle_mask(item_id):
    item = VaultItem.query.get_or_404(item_id)
    item.masked = not item.masked
    db.session.commit()
    return redirect(url_for('dashboard'))

#Delete Item Route
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    item = VaultItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

#Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

#Veridy Questions Route
@app.route('/verify_questions', methods=['GET', 'POST'])
def verify_questions():
    if 'user_id' not in session:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if request.method == 'GET':
        return render_template('verify_questions.html', user=user)

    answer1 = request.form.get('answer1').strip().lower()
    answer2 = request.form.get('answer2').strip().lower()
    answer3 = request.form.get('answer3').strip().lower()

    if (answer1 != user.security_a1.lower() or
        answer2 != user.security_a2.lower() or
        answer3 != user.security_a3.lower()):
        flash('Security question answers are incorrect.', 'danger')
        return redirect(url_for('verify_questions'))

    flash('Security questions verified successfully!', 'success')
    return redirect(url_for('dashboard'))

#Mark as Read Route
@app.route('/mark_as_read/<int:notification_id>', methods=['POST'])
def mark_as_read(notification_id):
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))
    
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != session['user_id']:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))

    notification.read = True
    db.session.commit()
    flash('Notification marked as read.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
