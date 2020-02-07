from flask import g, Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid

app = Flask(__name__, template_folder='templates')

#================ SETTING DATABASE =============================
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/myflask'
app.config["SECRET_KEY"] = "kjMsjdi21mdj24hqos0XasdjZ1238"
db = SQLAlchemy(app)
db.init_app(app)
#===============================================================


#================= LOGIN GUARD =================================
from flask_login import login_user, login_required, LoginManager, logout_user, current_user
login_manager = LoginManager()
login_manager.init_app(app)
#===============================================================

#================= MIGRATE =====================================
from models.user import UserApi
migrate = Migrate(app, db)
#===============================================================

#================= SEEDER ======================================
@app.cli.command("seeder")
def seed():
    from faker import Faker

    fake = Faker()
    for x in range(3):
        UserApi.seed(fake)
#===============================================================

#================= ROUTE =======================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == '' or password == '':
            flash("Enter a name and password")
            return redirect(url_for('index'))

        possible_user = UserApi.query.filter_by(email=email).first()
        if not possible_user:
            flash('Wrong username')
            return redirect(url_for('index'))

        if possible_user is not None and possible_user.verify_password(password):
            login_user(possible_user)
            return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/logout')
def user_logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
   return render_template('admin.html')

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login'))

#== ROUTE PAGE ==
@app.route('/user', methods=['GET', 'POST'])
def user():
    users = UserApi.query.all()
    return render_template('user.html', users=users)

@app.route('/user/add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'POST':
        user = UserApi(uuid = str(uuid.uuid4()), email=request.form['email'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user'))
    else:
        return render_template('user_add_edit.html')

@app.route('/user/<uuid>', methods=['GET', 'POST', 'DELETE'])
def user_edit(uuid):
    user = UserApi.query.filter_by(uuid=uuid).first()

    if request.form['_method'] == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('user'))

    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect(url_for('user'))

    if request.method == 'GET':
        return render_template('user_add_edit.html', user=user)
#===============================================================

if __name__ == '__main__':
    app.run(debug=True)