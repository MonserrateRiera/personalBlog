from flask import Blueprint, render_template, request, session, redirect, url_for
from services.auth_service import AuthService
from services.article_service import ArticleService

class BlogController:
    """
    BlogController handles all the routes and logic for the blog application.

    This class is responsible for managing user authentication, article management,
    and rendering the appropriate templates for each route.
    """

    def __init__(self, app):
        """
        Initializes the BlogController and registers all routes.

        Args:
            app (Flask): The Flask application instance.
        """
        self.auth_service = AuthService()
        self.article_service = ArticleService()
        self.app = app
        self.register_routes()

    def register_routes(self):
        """
        Registers all routes for the blog application.
        """
        self.app.add_url_rule("/login", view_func=self.login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", view_func=self.logout, methods=["GET"])
        self.app.add_url_rule("/", view_func=self.index, methods=["GET"])
        self.app.add_url_rule("/articles/<article_id>", view_func=self.show_article, methods=["GET"])
        self.app.add_url_rule("/admin/dashboard", view_func=self.dashboard, methods=["GET"])
        self.app.add_url_rule("/admin/new", view_func=self.new_article, methods=["GET", "POST"])
        self.app.add_url_rule("/admin/delete/<article_id>", view_func=self.delete_article, methods=["GET"])
        self.app.add_url_rule("/admin/edit/<article_id>", view_func=self.edit_article, methods=["GET", "POST"])

    def login(self):
        """
        Handles the login route.

        GET: Renders the login page if the user is not logged in.
        POST: Attempts to log in the user with the provided credentials.

        Returns:
            Response: The rendered login page or a redirect to the dashboard.
        """
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
        """
        Logs out the current user by clearing the session.

        Returns:
            Response: A redirect to the index page.
        """
        self.auth_service.try_logout()
        return redirect(url_for('index'))

    def index(self):
        """
        Renders the home page with a list of articles.

        Returns:
            Response: The rendered index page.
        """
        articles = self.article_service.get_article_list()
        username = session.get('username')
        return render_template('index.html', articles=articles, username=username)

    def show_article(self, article_id):
        """
        Displays a single article by its ID.

        Args:
            article_id (str): The ID of the article to display.

        Returns:
            Response: The rendered article page or a 404 error if not found.
        """
        article = self.article_service.get_article_by_id(article_id)
        if article:
            return render_template("article.html", article=article), 201
        else:
            return "Article not found.", 404

    @AuthService.login_required
    def dashboard(self):
        """
        Renders the admin dashboard with a list of articles.

        Returns:
            Response: The rendered dashboard page.
        """
        articles = self.article_service.get_article_list()
        return render_template("dashboard.html", articles=articles)

    @AuthService.login_required
    def new_article(self):
        """
        Handles the creation of a new article.

        GET: Renders the form to create a new article.
        POST: Creates a new article with the provided data.

        Returns:
            Response: A redirect to the index page or the form with an error message.
        """
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
        """
        Deletes an article by its ID.

        Args:
            article_id (str): The ID of the article to delete.

        Returns:
            Response: A redirect to the dashboard or the dashboard with an error message.
        """
        result = self.article_service.delete_article_by_id(article_id)
        if result:
            return redirect(url_for('dashboard'))
        articles = self.article_service.get_article_list()
        return render_template("dashboard.html", articles=articles, error=f"Something went wrong deleting the blog with id: {article_id}")

    @AuthService.login_required
    def edit_article(self, article_id):
        """
        Edits an article by its ID.

        GET: Renders the form to edit the article.
        POST: Updates the article with the provided data.

        Args:
            article_id (str): The ID of the article to edit.

        Returns:
            Response: A redirect to the dashboard or the form with an error message.
        """
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