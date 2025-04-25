from Article import Article
import json
import datetime

path = "articles.json"


def getArticleList():
    with open(path, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return []

        articles = [Article.fromJson(article_data) for article_data in data]
    return articles


def getAtricleById(article_id):
    articles = getArticleList()
    for article in articles: 
        if article.id == int(article_id):
            return article

    return None       

def createArticle(title:str, text:str) -> bool:
    if len(title)<3 and len(text) < 20:
        return False
    
    articles = getArticleList()
    newArticle = Article(title, datetime.date.today(), text)
    articles.append(newArticle)
    saveArticles(articles)
    return True


def saveArticles(articles):
    print(articles)
    with open(path, "w") as file:
        json.dump([article.toJson() for article in articles], file, indent=4)
    print("saved")


def deleteArticleById(id):
    articles = getArticleList()
    for article in articles:
        if article.id == int(id):
            articles.remove(article)
            saveArticles(articles)
            return articles
        
    return None    

def editArticleById(id, title, text):
   
    if len(title) < 3 or len(text) < 20:
        return None
     
    articles = getArticleList()
    for article in articles:
        if article.id == int(id):
            article.title = title
            article.text = text
            saveArticles(articles)
            return articles

    return None  # Devuelve None si no encuentra el artículo
