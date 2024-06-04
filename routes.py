from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from __init__ import app, db, login_manager

# ログイン状態を管理する
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


# LPページ
@app.route('/')
def index():
    return render_template('index.html')


# サインイン
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
            return render_template('signin.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # データベースからユーザーを取得
        from models import User
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # ログイン成功
            login_user(user)
            return redirect(url_for('userpage', current_user=current_user))
        else:   
            # ログイン失敗
            flash('メールアドレス、またはパスワードが間違っています')
            return redirect(url_for('signin'))

# ログアウト
@app.route('/logout')
@login_required  
def logout():
    logout_user()  
    return redirect(url_for('signin'))

# アカウント登録
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        # ユーザー情報を取得する
        from models import User
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # ユーザー情報をdbテーブルに保存する
        user = User(username=username, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('signin'))
        except:
            db.session.rollback()
            flash('そのメールアドレスはすでに登録されています')
            return render_template('signup.html')


# メインページ
@app.route('/userpage')
@login_required
def userpage():
    from models import Folder
    folders = Folder.query.filter_by(user_id=current_user.user_id).all()
    return render_template('userpage.html', folders=folders)

# フォルダから色を取得
# folder = Folder.query.first()
# print(folder.folder_color.color)  # フォルダの色を取得

# 色からフォルダを取得
# folder_color = FolderColor.query.first()
# for folder in folder_color.folders:
#     print(folder.folder_name)  # その色のフォルダ名を取得



# フォルダーを作成する
@app.route('/create_folder', methods=['GET', 'POST'])
def create_folder():
    if request.method == 'GET':
        return render_template('create_folder.html')
    if request.method == 'POST':
        # ユーザー情報を取得する
        from models import Folder
        title = request.form['title']
        color = request.form['color']
        # ユーザー情報をdbテーブルに保存する
        folder = Folder(user_id=current_user.user_id, folder_name=title, folder_color_id=color)
        try:
            db.session.add(folder)
            db.session.commit()
            return redirect(url_for('userpage'))
        except:
            db.session.rollback()
            flash('フォルダの作成中にエラーが発生しました')
            return url_for('userpage')

# urlを保存する
@app.route('/addUrl')
def add_url():
    return render_template('add_url.html')


# カラーテーブル変更用
@app.route('/color', methods=['GET', 'POST'])
def color():
    if request.method == 'GET':
        return render_template('color.html')
    if request.method == 'POST':
        # ユーザー情報を取得する
        from models import FolderColor
        colorname = request.form['colorname']
        # ユーザー情報をdbテーブルに保存する
        folder_color = FolderColor(color=colorname)
        try:
            db.session.add(folder_color)
            db.session.commit()
            return redirect(url_for('color'))
        except:
            db.session.rollback()
            flash('そのメールアドレスはすでに登録されています')
            return render_template('color.html')

