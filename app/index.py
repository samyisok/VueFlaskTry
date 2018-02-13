from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib
import json
import jwt
import datetime

from sqlalchemy.orm import relationship

app = Flask(__name__, static_url_path='')

app.config['DEBUG'] = True
app.config['secret'] = 'blablasec123'
app.config['salt'] = '123123'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://casino_user:casino123@localhost:5432/casino2'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    money = db.Column(db.Float, nullable=False)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer)
    cdate = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String)
    cdate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    data = db.Column(db.Integer)
    cdate = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class MsgTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1200), nullable=False)
    sender = db.Column(db.String(120), nullable=False)
    header = db.Column(db.String(120), nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_tpl_id = db.Column(db.Integer, db.ForeignKey('msg_template.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    cdate = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    msg_template = relationship("MsgTemplate")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'status': 'warning', 'message': 'token missing'})

        try:
            data = jwt.decode(token, app.config['secret'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'status': 'warning', 'message': 'token invalid'})

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
@token_required
def test(current_user):
    print(current_user)
    return jsonify({'status': 'success', 'message': 'wow so many text'})


@app.route('/new_messages_count', methods=['POST'])
@token_required
def new_messages_count(current_user):
    new_msg = Message.query.filter_by(user_id=current_user.id, status=1).count()
    return jsonify({'status': 'success', 'result': 'wow so many text', 'payload': new_msg})


@app.route('/messages', methods=['POST'])
@token_required
def messages(current_user):
    cur_user = User.query.filter_by(email=current_user.email).first()
    data = request.data
    info = json.loads(data)
    page = 1
    if 'page' in info['data']:
        page = info['data']['page']
    on_page = 10
    var = []
    msg_pagination = Message.query.filter_by(user_id=cur_user.id).paginate(page, on_page, False)
    for msg in msg_pagination.items:
        var1 = {'message': msg.msg_template.msg,
                'sender': msg.msg_template.sender,
                'title': msg.msg_template.header,
                'date': msg.cdate.isoformat(timespec='minutes', sep=' '),
                'id': msg.id,
                'status': msg.status}
        var.append(var1)
    print(var)
    all_pages = msg_pagination.pages
    return jsonify({'status': 'success', 'result': 'wow so many text', 'payload': var, 'pages': all_pages})


@app.route('/user')
def user():
    cur_user = User.query.filter_by(id=1).first()
    list = {"name": cur_user.email,
            "cash": cur_user.money}
    return jsonify(list)


@app.route('/login', methods=['POST'])
def login():
    data = request.data
    reg_info = json.loads(data)
    email = reg_info['data']['email']
    password = reg_info['data']['password'] + app.config['salt']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cur_user = User.query.filter_by(email=email, password=password_hash).first()
    if (cur_user):
        expire = datetime.datetime.now() + datetime.timedelta(minutes=150)
        data = {
            'email': cur_user.email,
            'exp': expire.timestamp()}
        print(data)
        token = jwt.encode(data, app.config['secret'], algorithm='HS256')
        return jsonify({'token': token.decode('UTF-8'), 'status': 'success'})
    else:
        warning = {'status': 'warning',
                   'message': 'Неверно задан пароль или пользователь.'}
        return jsonify(warning)


@app.route('/reg', methods=['POST'])
def reg():
    data = request.data
    reg_info = json.loads(data)
    email = reg_info['data']['email']
    cur_user = User.query.filter_by(email=email).first()
    if (cur_user):
        warning = {'status': 'warning',
                   'message': 'Такой пользователь уже существует'}
        return jsonify(warning)

    password = reg_info['data']['password'] + app.config['salt']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = User(email=email, password=password_hash, money=0)
    db.session.add(new_user)
    db.session.commit()
    welcome_id = 1
    new_message = Message(user_id=new_user.id, msg_tpl_id=welcome_id, status=1)
    db.session.add(new_message)
    db.session.commit()

    for i in range(1,400):
        msg = 'TestMsg#'+str(i)
        sender = 'Sender#'+str(i)
        header = 'Header#'+str(i)
        new_msg_template = MsgTemplate(msg=msg, sender=sender, header=header)
        db.session.add(new_msg_template)
        db.session.commit()
        new_test_message = Message(user_id=new_user.id, msg_tpl_id=new_msg_template.id, status=1)
        db.session.add(new_test_message)
        db.session.commit()

    list = {'status': 'success',
            'id': new_user.id}
    return jsonify(list)


# list = {"name": cur_user.name,
#         "cash": cur_user.money}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-access-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run()
