from __init__ import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    
    def get_id(self):
        return str(self.user_id)

    def is_active(self):
        return True

class FolderColor(db.Model):
    __tablename__ = 'folder_color'
    folder_color_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color = db.Column(db.String(255), nullable=False)

class Folder(db.Model):
    __tablename__ = 'folder'
    folder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    folder_name = db.Column(db.String(255), nullable=False)
    folder_color_id = db.Column(db.Integer, db.ForeignKey('folder_color.folder_color_id'), nullable=False)

    # ユーザーが持つフォルダへのリレーションシップ
    folder_color = db.relationship('FolderColor', backref='folders')

    __table_args__ = (db.UniqueConstraint('user_id', 'folder_name', name='unique_folder_name_per_user'),)


class Url(db.Model):
    __tablename__ = 'url'
    url_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.folder_id'), nullable=False)
    url = db.Column(db.String(2550), nullable=False)