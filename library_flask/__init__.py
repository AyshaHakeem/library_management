from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()
from library_flask.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from library_flask import routes