import json
import os


class ArticleRepository:
    def __init__(self):
        # Define the path to the JSON file where articles are stored
        self.__path = os.path.join(os.path.dirname(__file__), '../data/articles.json')

    def get_all_articles(self):
        """
        Reads all articles from the JSON file.
        
        Returns:
            list: A list of articles if the file is valid and exists.
                  Returns an empty list if the file is invalid or does not exist.
        """
        try:
            # Open the JSON file in read mode
            with open(self.__path, "r") as file:
                # Load the JSON data into a Python object
                data = json.load(file)
                return data
        except json.JSONDecodeError:
            # Handle the case where the JSON file is not properly formatted
            print("Error: The JSON file is not properly formatted.")
            return []
        except FileNotFoundError:
            # Handle the case where the JSON file does not exist
            print("Error: The JSON file does not exist. Returning an empty list.")
            return []

    def save_all(self, articles):
        """
        Saves all articles to the JSON file.
        
        Args:
            articles (list): A list of article objects to save. Each object must have a toJson() method.
        
        Raises:
            Exception: If an error occurs while saving the articles.
        """
        try:
            # Open the JSON file in write mode
            with open(self.__path, "w") as file:
                # Convert the list of articles to JSON and write it to the file
                json.dump([article.toJson() for article in articles], file, indent=4)
        except Exception as e:
            # Handle any exception that occurs during the save process
            print(f"Error while saving articles: {e}")
            raise