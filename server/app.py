from flask import Flask, redirect, url_for, render_template, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn

application = Flask(__name__, static_folder='lightshow-frontend/build/static/', template_folder='lightshow-frontend/build/')
application.config['SECRET_KEY'] = 'top secret!'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
application.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '416422595462913',
        'secret': '5cea25201b511b3b072de787db41182b'
    }
}

db = SQLAlchemy(application)
lm = LoginManager(application)
lm.login_view = 'index'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    priv_level = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(64), nullable=True)


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.String(64), primary_key=True)
    nickname = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(1024), nullable=True)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@application.route('/', methods=['GET'])
@application.route('/lights')
@application.route('/login')
@application.route('/signup')
def path_index():
    return render_template('index.html')

@application.route('/<path:path>')
def serve_path(path):
    return send_from_directory('/var/www/jesselupica', path)

@application.route('/static/<path:path>') # serve whatever the client requested in the static folder
def serve_static(path):
    return send_from_directory('lightshow-frontend/build/static', path)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@application.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@application.route('/test')
def test():
    return "Testing!"

if __name__ == '__main__':
    db.create_all()
    application.run(debug=True, host='0.0.0.0')
