from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime
from services.auth_service import tryLogin, tryLogout, loginRequired
from services.article_service import getArticleList, getAtricleById, createArticle, deleteArticleById, editArticleById

app = Flask(__name__)
app.secret_key="fsdfsd89ASDa.asdfsdfsd<z,s+asdasd"


@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET' and 'username' not in session:
        return render_template('login.html')
    elif request.method == 'POST' and 'username' not in session:
        username = request.form.get("username")
        password = request.form.get("password")
        result = tryLogin(username, password)
        if result:
            return redirect(url_for('dashboard'))
        
    return render_template('login.html', error="ERROR IN LOGIN")

@app.route("/logout", methods=['GET'])
def logout():
    tryLogout()  # Elimina 'username' de la sesión
    return redirect(url_for('index'))

@app.route("/", methods=['GET'])
def index():
    articles = getArticleList()
    username = session.get('username')  # Obtén el usuario de la sesión
    print(username)
    return render_template('index.html', articles=articles, username=username)

@app.route("/articles/<article_id>", methods=['GET'])
def showArticle(article_id):

    article = getAtricleById(article_id)
    if article:
        return render_template("article.html", article = article), 201
    else:
        return "Articulo no encontrado.", 404    

@app.route('/admin/dashboard', methods = ['GET'])
@loginRequired
def dashboard():
    articles = getArticleList()
    return render_template("dashboard.html", articles = articles)


@app.route("/admin/new", methods =["POST", "GET"])
@loginRequired
def newArticle():
    if request.method == "GET":
        return render_template("new_article_form.html", error = None)
    elif request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        result = createArticle(title, text)
        if result:
            return redirect(url_for('index'))
        else:
             return render_template("new_article_form.html", error = "Title or text lenght is too short!")
    return "ok"


@app.route("/admin/delete/<article_id>")
@loginRequired
def deleteArticle(article_id):
    result = deleteArticleById(article_id)
    if result:
        return redirect(url_for('dashboard'))
    articles = getArticleList()
    return render_template("dashboard.html", articles = articles, error = f"Something went wrong deleting the blog with id: {article_id}")


@app.route("/admin/edit/<article_id>",methods=["GET","POST"])
@loginRequired
def editArticle(article_id):
    if request.method == "GET":
        article = getAtricleById(article_id)
        if article:
            return render_template("edit_article_form.html", article = article)
        else:
            return "ERROR"
    elif "POST":
        
        title = request.form.get("title")
        text = request.form.get("text")

        result = editArticleById(article_id, title, text)

        if result:
            return redirect(url_for('dashboard'))
        articles = getArticleList()
        return render_template("dashboard.html", articles = articles, error = f"Something went wrong editing the blog with id: {article_id}")


if __name__ == "__main__":
    app.run(debug=True)