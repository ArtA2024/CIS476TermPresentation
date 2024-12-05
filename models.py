from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

# Initialize the database
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    master_password = db.Column(db.String(120), nullable=False)
    security_q1 = db.Column(db.String(120), nullable=False)
    security_a1 = db.Column(db.String(120), nullable=False)
    security_q2 = db.Column(db.String(120), nullable=False)
    security_a2 = db.Column(db.String(120), nullable=False)
    security_q3 = db.Column(db.String(120), nullable=False)
    security_a3 = db.Column(db.String(120), nullable=False)

    # Relationship to Notification
    notifications = relationship('Notification', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class VaultItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # e.g., 'Login', 'Credit Card', 'Identity'
    title = db.Column(db.String(255), nullable=False)

    # Fields for "Login"
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)

    # Fields for "Credit Card"
    credit_card_number = db.Column(db.String(16), nullable=True)
    cvv = db.Column(db.String(4), nullable=True)
    credit_card_expiration = db.Column(db.String(7), nullable=True)  # Format MM/YYYY

    # Fields for "Identity"
    full_name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    passport_number = db.Column(db.String(50), nullable=True)
    passport_expiration = db.Column(db.String(10), nullable=True)  # Format MM/DD/YYYY
    driver_license = db.Column(db.String(50), nullable=True)
    license_expiration = db.Column(db.String(10), nullable=True)  # Format MM/DD/YYYY
    ssn = db.Column(db.String(11), nullable=True)  # Social Security Number

    # Common fields
    secure_note = db.Column(db.Text, nullable=True)
    masked = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<VaultItem {self.title}>"

    def is_expired(self, expiration_date):
        """
        Check if an expiration date is past.
        """
        try:
            exp_date = datetime.strptime(expiration_date, '%m/%Y') if len(expiration_date) == 7 else datetime.strptime(expiration_date, '%m/%d/%Y')
            return exp_date < datetime.now()
        except ValueError:
            return False  # Invalid or missing date is not considered expired

    # Observer pattern
    def notify_observers(self):
        """
        Notify observers of relevant events (e.g., weak password, credit card expiration).
        """
        observers = [
            self.check_weak_password,
            self.check_credit_card_expiration,
            self.check_passport_expiration,
            self.check_license_expiration,
        ]
        for observer in observers:
            observer()

    def check_weak_password(self):
        """
        Notify if a Login item has a weak password.
        """
        if self.item_type == 'Login' and self.password and len(self.password) < 8:
            notification = Notification(
                user_id=self.user_id,
                message=f"Login '{self.title}' has a weak password."
            )
            db.session.add(notification)
            db.session.commit()

    def check_credit_card_expiration(self):
        """
        Notify if a Credit Card is expired.
        """
        if self.item_type == 'Credit Card' and self.credit_card_expiration and self.is_expired(self.credit_card_expiration):
            notification = Notification(
                user_id=self.user_id,
                message=f"Credit Card '{self.title}' has expired."
            )
            db.session.add(notification)
            db.session.commit()

    def check_passport_expiration(self):
        """
        Notify if a Passport is expired.
        """
        if self.item_type == 'Identity' and self.passport_expiration and self.is_expired(self.passport_expiration):
            notification = Notification(
                user_id=self.user_id,
                message=f"Passport for '{self.title}' has expired."
            )
            db.session.add(notification)
            db.session.commit()

    def check_license_expiration(self):
        """
        Notify if a Driver's License is expired.
        """
        if self.item_type == 'Identity' and self.license_expiration and self.is_expired(self.license_expiration):
            notification = Notification(
                user_id=self.user_id,
                message=f"Driver's License for '{self.title}' has expired."
            )
            db.session.add(notification)
            db.session.commit()


class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Notification {self.message}>"
