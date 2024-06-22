from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_login import UserMixin
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from urllib.parse import urlparse
from sqlalchemy import null
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'signin'

# モデルのインポート
from model import User, Folder, Url
# ルートのインポート
import routes

# SQLiteエンジンの作成時に外部キー制約を有効にする
def enable_foreign_keys():
    if 'sqlite' in db.engine.url.drivername:
        with db.engine.connect() as con:
            con.execute('PRAGMA foreign_keys=ON')

# アプリケーションコンテキスト内でデータベースを作成
with app.app_context():
    db.create_all()