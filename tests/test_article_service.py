import pytest
from personal_blog.services import ArticleService
from personal_blog.model.Article import Article

# Fake repository for testing
class FakeRepository:
    def __init__(self):
        self.articles = []

    def load_articles(self):
        return self.articles

    def save_articles(self, articles):
        self.articles = articles

@pytest.fixture
def service():
    repo = FakeRepository()
    return ArticleService(repo)

def test_create_article(service):
    article = service.create_article("Test Title", "Test Content")
    assert article.title == "Test Title"
    assert article.content == "Test Content"
    assert article.id == 1

def test_get_article_by_id(service):
    service.create_article("Title 1", "Content 1")
    article = service.get_article_by_id(1)
    assert article is not None
    assert article.title == "Title 1"

def test_delete_article(service):
    service.create_article("Title 1", "Content 1")
    service.delete_article(1)
    assert service.get_article_by_id(1) is None