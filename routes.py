from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exchange.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Session(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(amount=form.amount.data, currency=form.currency.data, price=form.price.data, user=current_user)
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders'))
    return render_template('new_order.html', form=form)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/transactions/new', methods=['GET', 'POST'])
@login_required
def new_transaction():
    form = PaymentForm()
    if form.validate_on_submit():
        transaction = Transaction(amount=form.amount.data, currency=form.currency.data, user=current_user)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transactions'))
    return render_template('new_transaction.html', form=form)

@socketio.on('connect')
def connect():
    print('Client connected')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('new_order')
def new_order(data):
    order = Order(amount=data['amount'], currency=data['currency'], price=data['price'], user=current_user)
    db.session.add(order)
    db.session.commit()
    emit('new_order', data)

@socketio.on('new_transaction')
def new_transaction(data):
    transaction = Transaction(amount=data['amount'], currency=data['currency'], user=current_user)
    db.session.add(transaction)
    db.session.commit()
    emit('new_transaction', data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
