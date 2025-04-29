from flask import Blueprint, render_template, request, session, redirect, url_for
from personal_blog.services.auth_service import AuthService
from personal_blog.services.article_service import ArticleService

class BlogController:
    """
    BlogController handles all the routes and logic for the blog application.
    """

    def __init__(self, app):
        self.auth_service = AuthService()
        self.article_service = ArticleService()
        self.app = app
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule("/login", view_func=self.login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", view_func=self.logout, methods=["GET"])
        self.app.add_url_rule("/", view_func=self.index, methods=["GET"])
        self.app.add_url_rule("/articles/<article_id>", view_func=self.show_article, methods=["GET"])
        self.app.add_url_rule("/admin/dashboard", view_func=self.dashboard, methods=["GET"])
        self.app.add_url_rule("/admin/new", view_func=self.new_article, methods=["GET", "POST"])
        self.app.add_url_rule("/admin/delete/<article_id>", view_func=self.delete_article, methods=["GET"])
        self.app.add_url_rule("/admin/edit/<article_id>", view_func=self.edit_article, methods=["GET", "POST"])

    def login(self):
        if request.method == 'GET' and 'username' not in session:
            return render_template('login.html')
        elif request.method == 'POST' and 'username' not in session:
            username = request.form.get("username")
            password = request.form.get("password")
            result = self.auth_service.try_login(username, password)
            if result:
                return redirect(url_for('dashboard'))
        return render_template('login.html', error="ERROR IN LOGIN")

    def logout(self):
        self.auth_service.try_logout()
        return redirect(url_for('index'))

    def index(self):
        articles = self.article_service.get_article_list()
        username = session.get('username')
        return render_template('index.html', articles=articles, username=username)

    def show_article(self, article_id):
        article = self.article_service.get_article_by_id(article_id)
        if article:
            return render_template("article.html", article=article), 201
        else:
            return "Article not found.", 404

    @AuthService.login_required
    def dashboard(self):
        articles = self.article_service.get_article_list()
        return render_template("dashboard.html", articles=articles)

    @AuthService.login_required
    def new_article(self):
        if request.method == "GET":
            return render_template("new_article_form.html", error=None)
        elif request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")
            result = self.article_service.create_article(title, text)
            if result:
                return redirect(url_for('index'))
            else:
                return render_template("new_article_form.html", error="Title or text length is too short!")
        return "ok"

    @AuthService.login_required
    def delete_article(self, article_id):
        result = self.article_service.delete_article_by_id(article_id)
        if result:
            return redirect(url_for('dashboard'))
        articles = self.article_service.get_article_list()
        return render_template("dashboard.html", articles=articles, error=f"Something went wrong deleting the blog with id: {article_id}")

    @AuthService.login_required
    def edit_article(self, article_id):
        if request.method == "GET":
            article = self.article_service.get_article_by_id(article_id)
            if article:
                return render_template("edit_article_form.html", article=article)
            else:
                return "ERROR"
        elif request.method == "POST":
            title = request.form.get("title")
            text = request.form.get("text")
            result = self.article_service.edit_article_by_id(article_id, title, text)
            if result:
                return redirect(url_for('dashboard'))
            articles = self.article_service.get_article_list()
            return render_template("dashboard.html", articles=articles, error=f"Something went wrong editing the blog with id: {article_id}")


# --- Esta función es para TESTING, no para producción ---
def register_routes(article_service):
    from flask import Blueprint, jsonify, request

    article_bp = Blueprint("article", __name__)

    @article_bp.route("/articles", methods=["GET"])
    def get_articles():
        return jsonify(article_service.get_article_list())

    @article_bp.route("/articles", methods=["POST"])
    def create_article():
        data = request.get_json()
        article = article_service.create_article(data["title"], data["content"])
        return jsonify(article), 201

    @article_bp.route("/articles/<int:article_id>", methods=["GET"])
    def get_article(article_id):
        article = article_service.get_article_by_id(article_id)
        if article:
            return jsonify(article)
        else:
            return "Article not found", 404

    return article_bp
