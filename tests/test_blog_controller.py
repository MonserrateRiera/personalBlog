import pytest
from flask import Flask
from personal_blog.controllers.blog_controller import init_article_routes
from personal_blog.services.article_service import ArticleService

class FakeRepository:
    def __init__(self):
        self.articles = []

    def load_articles(self):
        return self.articles

    def save_articles(self, articles):
        self.articles = articles

@pytest.fixture
def client():
    app = Flask(__name__)
    repo = FakeRepository()
    service = ArticleService(repo)
    article_bp = init_article_routes(service)
    app.register_blueprint(article_bp)
    return app.test_client()

def test_get_articles_empty(client):
    response = client.get('/articles')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_article(client):
    response = client.post('/articles', json={'title': 'Test', 'content': 'Testing'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test'
    assert data['content'] == 'Testing'

def test_get_article_by_id(client):
    client.post('/articles', json={'title': 'Test', 'content': 'Testing'})
    response = client.get('/articles/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1