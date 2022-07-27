from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UploadFileForm, FilterByCityForm, FilterByPriceForm, FilterByQuantityForm, FilterByDateForm
from app.models import User, Data
from flask_login import login_user, current_user, logout_user, login_required
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import pandas as pd


posts = [

	{
		'author': 'Cory Schafer',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date_posted': '23 July 2022'

	},
	{
		'author': 'Jane Doe',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': '22 July 2022'

	}
]

@app.route("/")
def home():
	data = Data.query.paginate(per_page=3)
	return render_template('home.html', data=data)


@app.route("/about")
def about():
	return render_template('about.html',title='About')


@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your Account has been created! You are now able to log in','success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			if user and bcrypt.check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				next_page = request.args.get(next)
				return redirect(next_page) if next_page else redirect(url_for('home'))
			else:
				flash('Login Unsuccessful. Please check email and password','danger')
	return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/upload",methods=['GET','POST'])
@login_required
def upload():
	form = UploadFileForm()
	if form.validate_on_submit():
		file = form.file.data
		file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
		file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
		parseCSV(file_path)
		flash('Your File Contents have been added to the DB','success')
		return redirect(url_for('home'))

	return render_template('upload.html',title='Upload',form=form)



def parseCSV(filePath):
	col_names = ['transaction_id','transaction_time','product_name','quantity','unit_price','total_price','delivered_to_city']
	csvData = pd.read_csv(filePath,names=col_names,header=None)
	data = []
	for i,row in csvData.iterrows():
		# print(row)
		temp = []
		temp.append(row['transaction_id'])
		temp.append(row['transaction_time'])
		temp.append(row['product_name'])
		temp.append(row['quantity'])
		temp.append(row['unit_price'])
		temp.append(row['total_price'])
		temp.append(row['delivered_to_city'])
		data.append(temp)

	cnt = 1;
	for l in data:
		if(cnt==1):
			cnt = cnt+1
			continue
		else:
			data = Data(transaction_id=l[0],transaction_time=l[1],product_name=l[2],quantity=l[3],unit_price=l[4],total_price=l[5],delivered_to_city=l[6])
			db.session.add(data)
			db.session.commit()
		# data = Data()
		# db.session.add(data)
		# db.session.commit()

@app.route("/delete/<int:transaction_id>")
@login_required
def delete_entry(transaction_id):
	data = Data.query.get(transaction_id)
	db.session.delete(data)
	db.session.commit()
	flash(f"Entry with {transaction_id} has been deleted!",'success')
	return redirect(url_for('home'))	


@app.route("/filterByCity",methods=['GET','POST'])
@login_required
def filterByCity():
	form = FilterByCityForm()
	city = form.city_name.data
	da = Data.query.filter_by(delivered_to_city=city)
	if form.validate_on_submit():
		return render_template('filterByCity.html',title='Filter',form=form,da=da)
	return render_template('filterByCity.html',title='Filter',form=form,da=da)

@app.route("/filterByPrice",methods=['GET','POST'])
@login_required
def filterByPrice():
	form = FilterByPriceForm()
	price = form.total_price_range.data
	da = Data.query.filter_by(total_price=price)
	if form.validate_on_submit():
		return render_template('filterByPrice.html',title='Filter',form=form,da=da)
	return render_template('filterByPrice.html',title='Filter',form=form,da=da)


@app.route("/filterByQuantity",methods=['GET','POST'])
@login_required
def filterByQuantity():
	form = FilterByQuantityForm()
	quantity = form.quantity_range.data
	da = Data.query.filter_by(quantity=quantity)
	if form.validate_on_submit():
		return render_template('filterByQuantity.html',title='Filter',form=form,da=da)
	return render_template('filterByQuantity.html',title='Filter',form=form,da=da)

@app.route("/filterByDate",methods=['GET','POST'])
@login_required
def filterByDate():
	form = FilterByDateForm()
	date = form.date_range.data
	search = "{}%".format(date)
	da = Data.query.filter(Data.transaction_time.like(search)).all()
	if form.validate_on_submit():
		return render_template('filterByDate.html',title='Filter',form=form,da=da)
	return render_template('filterByDate.html',title='Filter',form=form,da=da)
