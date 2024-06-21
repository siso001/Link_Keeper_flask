from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from __init__ import app, db, login_manager
from urllib.parse import urlparse
from sqlalchemy import null

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
    from models import Folder, Url
    folders = Folder.query.filter_by(user_id=current_user.user_id).all()
    url_count = Url.query.count()
    return render_template('userpage.html',folders=folders, url_count=url_count)

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
@app.route('/addUrl', methods=['GET', 'POST'])
def add_url():
    if request.method == 'GET':
        from models import Folder
        folders = Folder.query.filter_by(user_id=current_user.user_id).all() # ログインしているユーザーのIDからフォルダ情報を取得する
        return render_template('add_url.html', folders=folders)
    if request.method == 'POST':
        # ユーザー情報を取得する
        from models import Url
        url = request.form['url']
        name = request.form['name']
        domain = urlparse(url).netloc.replace('www.', '')
        folder_id = request.form['folder']
        # ユーザー情報をdbテーブルに保存する
        url = Url(user_id=current_user.user_id, url=url, url_name=name, domain=domain, folder_id=folder_id)
        try:
            db.session.add(url)
            db.session.commit()
            from models import Folder
            folder = Folder.query.get(folder_id)
            if folder:
                return redirect(url_for('folder', folder_id=folder_id, folder_name=folder.folder_name))
            else:
                return redirect(url_for('add_url'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_url'))

# urlをフォルダに保存
@app.route('/addUrl-toFolder', methods=['GET', 'POST'])
def add_url2():
    if request.method == 'GET':
        from models import Folder, Url
        # ログインしているユーザーのIDからフォルダ、URL情報を取得する
        folders = Folder.query.filter_by(user_id=current_user.user_id).all() 
        urls = Url.query.filter_by(user_id=current_user.user_id, folder_id=0).all()
        return render_template('add_url-to_folder.html', folders=folders, urls=urls)
    if request.method == 'POST':
        # ユーザー情報を取得する
        from models import Url
        url = request.form['url']
        folder_id = request.form['folder']
        url_record = db.session.query(Url).get(url) 
        url_record.folder_id = folder_id
        try:
            db.session.commit()
            from models import Folder
            folder = Folder.query.get(folder_id)
            if folder:
                return redirect(url_for('folder', folder_id=folder_id, folder_name=folder.folder_name))
            else:
                return redirect(url_for('add_url2'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_url2'))


# フォルダを削除する
@app.route('/delete_folder', methods=['GET', 'POST'])
def delete_folder():
    if request.method == 'GET':
        from models import Folder
        folders = Folder.query.filter_by(user_id=current_user.user_id).all() # ログインしているユーザーのIDからフォルダ情報を取得する
        return render_template('delete_folder.html', folders=folders)
    if request.method == 'POST':
        from models import Folder
        folder_id = request.form['folder']
        folder = db.session.query(Folder).get(folder_id)
        db.session.delete(folder)
        db.session.commit()
        return redirect(url_for('userpage'))

# urlを削除する
@app.route('/delete_url', methods=['GET', 'POST'])
def delete_url():
    if request.method == 'GET':
        return render_template('delete_url.html')
    if request.method == 'POST':
        pass
        # from models import Folder
        # folder_id = request.form['folder']
        # folder = db.session.query(Folder).get(1)
        # try:
        #     db.session.delete(folder)
        #     db.session.commit()
        #     from models import Folder
        #     folder = Folder.query.get(folder_id)
        #     if folder:
        #         return redirect(url_for('another_folder', folder_id=folder_id, folder_name=folder.folder_name))
        #     else:
        #         return redirect(url_for('add_url'))
        # except Exception as e:
        #     db.session.rollback()
        #     flash(f'Error: {str(e)}', 'danger')
        #     return redirect(url_for('add_url'))

# 登録してある全てのurlを閲覧する
@app.route('/userpage/allurl', endpoint='allurl', methods=['GET', 'POST'])
def view_all_urls():
    if request.method == 'GET':
        from models import Folder, Url
        folder_name = "all_url"
        all_urls = db.session.query(Url, Folder.folder_name).join(Folder, Url.folder_id == Folder.folder_id).all()
        if all_urls:
            color = "gray"
            return render_template('views_all_url.html', folder=folder, urls=all_urls, color=color, folder_name=folder_name)
        else:
            # フォルダが見つからない場合の処理
            return "Folder not found", 404
    if request.method == 'POST':
        data = request.get_json()
        url_id = data.get('url_id')
        from models import Url
        url = db.session.query(Url).get(url_id)
        if url:
            db.session.delete(url)
            db.session.commit()
            return redirect(url_for('view_all_urls', folder_name=folder_name))

# フォルダ内のurlを閲覧する
@app.route('/userpage/<int:folder_id>/<folder_name>', endpoint='folder', methods=['GET', 'POST'])
def folder(folder_id, folder_name):
    if request.method == 'GET':
        from models import Folder, Url
        folder_name = folder_name.replace('<br>', ' ')
        folder = Folder.query.filter_by(folder_id=folder_id).first()
        if folder:
            urls = folder.urls.all()
            color = folder.folder_color.color
            return render_template('views_folder.html', folder=folder, urls=urls, color=color, folder_id=folder_id, folder_name=folder_name)
        else:
            # フォルダが見つからない場合の処理
            return "Folder not found", 404
    if request.method == 'POST':
        data = request.get_json()
        url_id = data.get('url_id')
        from models import Url
        url = db.session.query(Url).get(url_id)
        if url:
            db.session.delete(url)
            db.session.commit()
            return redirect(url_for('folder', folder_id=folder_id, folder_name=folder_name))

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
