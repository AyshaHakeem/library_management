from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from library_flask.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()

def create_app(config_call=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    
    from library_flask.users.routes import users
    from library_flask.members.routes import members
    from library_flask.books.routes import books
    from library_flask.transactions.routes import transactions
    app.register_blueprint(users)
    app.register_blueprint(members)
    app.register_blueprint(books)
    app.register_blueprint(transactions)

    return app





