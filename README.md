# Milestone 4 Flask Application

## Overview
This project is a Flask web application designed to manage user authentication and provide an admin dashboard. It utilizes a SQLite database to store user data and other relevant information.

## Project Structure
```
milestone4
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── static
│   │   ├── css
│   │   ├── js
│   │   └── uploads
│   └── templates
│       ├── admin.html
│       ├── dashboard4.html
│       ├── login4.html
│       └── register4.html
├── instance
│   └── database.db
├── main4.py
├── wsgi.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd milestone4
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add the necessary environment variables, such as:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///instance/database.db
   ```

5. **Run the application:**
   ```
   python main4.py
   ```

6. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Deployment
To deploy the application, follow the instructions in the `Procfile` and ensure that the correct Python version is specified in `runtime.txt`.

## Features
- User registration and login
- Admin dashboard for managing users
- File uploads

## License
This project is licensed under the MIT License.