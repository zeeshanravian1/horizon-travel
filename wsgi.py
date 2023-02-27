from flask import Flask
from flask_login import LoginManager
from flask_toastr import Toastr
app = Flask(__name__)

login_manager = LoginManager()

login_manager.init_app(app)

toastr = Toastr(app)