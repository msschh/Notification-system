
from flask import Flask, render_template, url_for, redirect, request
from flask_login import UserMixin, current_user, login_user, logout_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

import db
from pathlib import Path
import json
import fmi_interaction as fmi
from firebase import FirebaseServer, FIREBASE_API_TOKEN

import helper as hp

app = Flask(__name__)
database = None

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
data_base = SQLAlchemy(app)

class User(UserMixin, data_base.Model):
    __tablename__ = "users"
    id = data_base.Column(data_base.Integer, primary_key=True)
    fname = data_base.Column(data_base.String(64), index=True, unique=False)
    lname = data_base.Column(data_base.String(64), index=True, unique=False)
    email = data_base.Column(data_base.String(64), index=True, unique=True)
    group = data_base.Column(data_base.String(10), index=True, unique=False, default=None)
    is_admin = data_base.Column(data_base.Integer, unique=False, default=0)
    is_teacher = data_base.Column(data_base.Integer, unique=False, default=0)
    is_student = data_base.Column(data_base.Integer, unique=False, default=0)

def init():
    global database
    config_file = Path(Path(__file__).parent/'data.config')
    with config_file.open() as f:
        data = f.read()
    config = json.loads(data)
    database = db.DataBase(config['database'], config['username'], config['password'])


app.before_first_request(init)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
def base():
    return redirect(url_for("home"))


@app.route("/home/")
def home():
    return render_template("home.html")


@app.route("/unread_news/")
@login_required
def unread_news():
    news = database.read_unread_news(current_user.group, current_user.email, current_user.is_teacher)
    return render_template("news.html", news=news)


@app.route("/news/")
@login_required
def news():
    if current_user.is_teacher:
        teacher_name = hp.getFullName(current_user.fname, current_user.lname)
        news = database.read_all_news(current_user.group, teacher_name)
    else:
        news = database.read_all_news(current_user.group)
    return render_template("news.html", news=news)


@app.route("/news/add/")
@login_required
def newsAdd():
    grupe = fmi.get_groups(is_admin=current_user.is_admin, is_teacher=current_user.is_teacher)
    return render_template("news_add.html", grupe=grupe)


@app.route("/news/create/", methods = ['POST'])
@login_required
def newsCreate():
    news = {}
    news['text'] = request.form['text']
    news['start_date'] = request.form['start_date']
    news['end_date'] = request.form['end_date']
    news['groups'] = request.form.getlist('grupe')
    news['author'] = hp.getFullName(current_user.fname, current_user.lname)
    news_id = database.add_news(json.dumps(news))


    server = FirebaseServer(FIREBASE_API_TOKEN)
    for grupa in news['groups']:
        tokens = database.get_tokens(grupa)

        if tokens == []:
            continue

        server.send("Mesaj nou", "in grupa " + grupa, tokens)

    return redirect(url_for("newsView", id=str(news_id)))


@app.route("/news/edit/<id>/")
@login_required
def newsEdit(id):
    news = database.read_news(id)
    return render_template("news_edit.html", news=news)


@app.route("/news/update/", methods = ['POST'])
@login_required
def newsUpdate():
    news = {}
    news['news_id'] = request.form['news_id']
    news['text'] = request.form['text']
    news['start_date'] = request.form['start_date']
    news['end_date'] = request.form['end_date']
    news = database.update_news(json.dumps(news))
    return redirect(url_for("newsView", id=request.form['news_id']))


@app.route("/news/view/<id>/")
@login_required
def newsView(id):
    database.add_user_news(id, current_user.email)
    news = database.read_news(id)
    return render_template("news_view.html", news=news)


@app.route("/news/delete/<id>/")
@login_required
def newsDelete(id):
    database.delete_news(id)
    return redirect(url_for("news"))


@app.route("/groups/")
@login_required
def groups():
    return render_template("groups.html")


@app.route("/notifications/")
@login_required
def notifications():
    return render_template("notifications.html")

@app.route("/login/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return redirect("http://127.0.0.1:10000/auth_user_normal?client_id=3&redirect_uri=http://127.0.0.1:11000/callback")

@app.route("/login2/")
def login2():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return redirect("http://127.0.0.1:10000/auth_admin?client_id=3&redirect_uri=http://127.0.0.1:11000/callback")

@app.route("/login_teacher/")
def login_teacher():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    return redirect("http://127.0.0.1:10000/auth_profesor?client_id=3&redirect_uri=http://127.0.0.1:11000/callback")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/callback")
def callback_method():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    fname = request.args.get("fname")
    lname = request.args.get("lname")
    email = request.args.get("email")
    is_admin = request.args.get("is_admin")
    is_teacher = request.args.get("is_teacher")
    is_student = request.args.get("is_student")
    group  = request.args.get("group", None)
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(fname=fname, lname=lname, email=email, is_admin=is_admin, is_teacher=is_teacher, is_student=is_student, group=group)
        data_base.session.add(user)
        data_base.session.commit()
    login_user(user, remember=False)
    return redirect(url_for("home"))


@app.route("/phone", methods=["POST", "GET"])
def phone_method():
    import pprint as pp
    token = request.args['token']
    grupa = request.args['grupa']
    add = database.add_token(grupa, token)
    print (add)
    return jsonify(add)

if __name__ == "__main__":
    data_base.drop_all()
    data_base.create_all()
    app.run(port=11000, debug=True, host="0.0.0.0")
