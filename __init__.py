from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'signin'

# モデルのインポート
from models import User, Folder, Url
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

if __name__ == '__main__':
    app.run(debug=True)