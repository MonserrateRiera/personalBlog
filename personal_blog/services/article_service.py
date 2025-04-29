from personal_blog.model.Article import Article
from personal_blog.repository.article_repository import ArticleRepository
import datetime


class ArticleService:
    def __init__(self):
        """
        Initializes the ArticleService with an instance of ArticleRepository.
        """
        self.__article_repository = ArticleRepository()

    def get_article_list(self):
        """
        Retrieves all articles from the repository.

        Returns:
            list: A list of Article objects.
        """
        data = self.__article_repository.get_all_articles()
        articles = [Article.fromJson(article_data) for article_data in data]
        return articles

    def get_article_by_id(self, article_id):
        """
        Retrieves a single article by its ID.

        Args:
            article_id (int): The ID of the article to retrieve.

        Returns:
            Article: The article with the specified ID, or None if not found.
        """
        articles = self.get_article_list()
        for article in articles:
            if article.id == int(article_id):
                return article
        return None

    def create_article(self, title: str, text: str) -> bool:
        """
        Creates a new article and saves it to the repository.

        Args:
            title (str): The title of the article.
            text (str): The content of the article.

        Returns:
            bool: True if the article was created successfully, False otherwise.
        """
        if len(title) < 3 or len(text) < 20:
            return False

        articles = self.get_article_list()
        new_article = Article(title, datetime.date.today(), text)
        articles.append(new_article)
        self.__article_repository.save_all(articles)
        return True

    def delete_article_by_id(self, article_id):
        """
        Deletes an article by its ID.

        Args:
            article_id (int): The ID of the article to delete.

        Returns:
            bool: True if the article was deleted successfully, False otherwise.
        """
        articles = self.get_article_list()
        for article in articles:
            if article.id == int(article_id):
                articles.remove(article)
                self.__article_repository.save_all(articles)
                return True
        return False

    def edit_article_by_id(self, article_id, title, text):
        """
        Edits an existing article by its ID.

        Args:
            article_id (int): The ID of the article to edit.
            title (str): The new title of the article.
            text (str): The new content of the article.

        Returns:
            bool: True if the article was edited successfully, False otherwise.
        """
        if len(title) < 3 or len(text) < 20:
            return False

        articles = self.get_article_list()
        for article in articles:
            if article.id == int(article_id):
                article.title = title
                article.text = text
                self.__article_repository.save_all(articles)
                return True
        return False