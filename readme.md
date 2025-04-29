# Personal Blog (Flask)

This is a small personal blog API built with Flask.  
The project is designed to apply clean code principles, dependency injection, modular architecture, and good development practices.
I've found this project at https://roadmap.sh/projects/personal-blog
## 📚 Project Structure

personalBlog/   


│ ├── app.py # Application entry point   
├── controllers/   
│ └── article_controller.py # Route handlers (Blueprint)  
├── services/   
│ └── article_service.py # Business logic   
├── repositories/   
│ └── article_repository.py # Data access layer (JSON file)   
├── models/   
│ └── article.py # Article model   
├── data/   
│ └── articles.json # Articles data file   
└── templates/ # (Optional) HTML templates  


## ✨ Features

- Create a new article
- Retrieve all articles
- Retrieve a single article by ID
- Update an existing article
- Delete an article
- Persistent storage using a local JSON file
- Clean and modular project structure
- Manual dependency injection

## 🛠️ Technologies Used

- **Python 3.11+**
- **Flask**
- **JSON** (for data storage)

## 🚀 How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/MonserrateRiera/personalBlog.git
    cd personalBlog
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install flask
    ```

3. Run the application:
    ```bash
    python app.py
    ```

4. The server will start at `http://127.0.0.1:5000/`

## 🛤️ API Endpoints

| Method | Endpoint                   | Description            |
|:-------|:----------------------------|:-----------------------|
| GET    | `/articles`                 | Get all articles        |
| GET    | `/articles/<id>`            | Get a single article    |
| POST   | `/articles`                 | Create a new article    |
| PUT    | `/articles/<id>`            | Update an article       |
| DELETE | `/articles/<id>`            | Delete an article       |

## ⚙️ Future Improvements

- Add input validation
- Implement error handling and better response messages
- Write unit tests for services and controllers
- Replace JSON with a real database (SQLite, PostgreSQL)
- Add user authentication

## 🤝 Contributing

Pull requests are welcome! Feel free to open an issue to discuss improvements or new features.

## 📄 License

This project is open-source and free to use.

---

# 🙌 Author

Made with passion by [Monserrate Riera](https://github.com/MonserrateRiera)

