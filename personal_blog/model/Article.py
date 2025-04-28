import datetime, random
from datetime import date

class Article:
    def __init__(self, title: str, date: datetime.date, text: str, id: int = None):
        self.__id = id if id is not None else random.randint(1, 5000)
        self.__title = title
        self.__date = date 
        self.__text = text



    @property
    def title(self) -> str:
        return self.__title       
    @property
    def date(self) -> date:
        return self.__date      
    @property
    def text(self) -> str:
        return self.__text
    
    @property
    def id(self) -> int:
        return self.__id
    

    @title.setter
    def title(self, title):
        self.__title = title      

    @text.setter
    def text(self, text):
        self.__text = text

    @date.setter
    def date(self, date):
        self.__date = date      

    def toJson(self) -> dict[str,str]:
        """ Conviert the object into a dictionary """
        return{
            "id": self.__id,
            "title": self.__title,
            "date": self.__date.strftime("%Y-%m-%d"),
            "text": self.__text
        }
    
    @classmethod
    def fromJson(cls, data: dict[str, str]) -> "Article":
        return cls(
            id=data["id"],
            title=data["title"],
            date=datetime.datetime.strptime(data["date"], "%Y-%m-%d").date(),
            text=data["text"]
        )