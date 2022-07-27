from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}','{self.email}')"


class Data(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	transaction_id = db.Column(db.String(15),unique=True,nullable=False)
	transaction_time = db.Column(db.String(15),nullable=False)
	product_name = db.Column(db.String(20),nullable=False)
	quantity = db.Column(db.Integer(),nullable=False)
	unit_price = db.Column(db.Float(),nullable=False)
	total_price = db.Column(db.Float(),nullable=False)
	delivered_to_city = db.Column(db.String(20),nullable=False)


db.create_all() 