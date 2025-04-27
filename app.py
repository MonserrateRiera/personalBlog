from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from services.auth_service import AuthService
from services.article_service import ArticleService
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Initialize services
auth_service = AuthService()
article_service = ArticleService()

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and 'username' not in session:
        return render_template('login.html')
    elif request.method == 'POST' and 'username' not in session:
        username = request.form.get("username")
        password = request.form.get("password")
        result = auth_service.try_login(username, password)
        if result:
            return redirect(url_for('dashboard'))
    return render_template('login.html', error="ERROR IN LOGIN")

@app.route("/logout", methods=['GET'])
def logout():
    auth_service.try_logout()  # Removes 'username' from the session
    return redirect(url_for('index'))

@app.route("/", methods=['GET'])
def index():
    articles = article_service.get_article_list()
    username = session.get('username')  # Get the username from the session
    return render_template('index.html', articles=articles, username=username)

@app.route("/articles/<article_id>", methods=['GET'])
def showArticle(article_id):
    article = article_service.get_article_by_id(article_id)
    if article:
        return render_template("article.html", article=article), 201
    else:
        return "Article not found.", 404

@app.route('/admin/dashboard', methods=['GET'])
@AuthService.login_required
def dashboard():
    articles = article_service.get_article_list()
    return render_template("dashboard.html", articles=articles)

@app.route("/admin/new", methods=["POST", "GET"])
@AuthService.login_required
def newArticle():
    if request.method == "GET":
        return render_template("new_article_form.html", error=None)
    elif request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        result = article_service.create_article(title, text)
        if result:
            return redirect(url_for('index'))
        else:
            return render_template("new_article_form.html", error="Title or text length is too short!")
    return "ok"

@app.route("/admin/delete/<article_id>")
@AuthService.login_required
def deleteArticle(article_id):
    result = article_service.delete_article_by_id(article_id)
    if result:
        return redirect(url_for('dashboard'))
    articles = article_service.get_article_list()
    return render_template("dashboard.html", articles=articles, error=f"Something went wrong deleting the blog with id: {article_id}")

@app.route("/admin/edit/<article_id>", methods=["GET", "POST"])
@AuthService.login_required
def editArticle(article_id):
    if request.method == "GET":
        article = article_service.get_article_by_id(article_id)
        if article:
            return render_template("edit_article_form.html", article=article)
        else:
            return "ERROR"
    elif request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        result = article_service.edit_article_by_id(article_id, title, text)
        if result:
            return redirect(url_for('dashboard'))
        articles = article_service.get_article_list()
        return render_template("dashboard.html", articles=articles, error=f"Something went wrong editing the blog with id: {article_id}")

if __name__ == "__main__":
    app.run(debug=True)