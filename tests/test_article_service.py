import unittest
from flask import Flask, session
from services.article_service import ArticleService

class TestArticleService(unittest.TestCase):
    def setUp(self):
        # Set up a Flask app context for testing
        self.article_service = ArticleService()

    def test_getarticle_list(self):
        articles = self.article_service.get_article_list()
        self.assertIsInstance(articles, list)



if __name__ == "__main__":
    unittest.main()