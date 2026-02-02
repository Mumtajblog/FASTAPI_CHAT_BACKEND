# FastAPI Chat Application

This is a simple chat application built with FastAPI. It provides a RESTful API for user authentication, creating chat sessions, and exchanging messages. The project uses a SQLite database for data storage.

## Prerequisites

*   Python 3.8 or newer.

## Design Decisions

*   **Framework**: FastAPI was chosen for its high performance, asynchronous support, and automatic API documentation.
*   **Database**: SQLite is used for its simplicity and serverless nature, making it easy to set up and run the application locally. For a production environment, a more robust database like PostgreSQL would be recommended.
*   **Authentication**: JWT (JSON Web Tokens) are used to secure the session and message-related API endpoints.
*   **ORM**: SQLAlchemy is used as the Object-Relational Mapper to interact with the database, providing a high-level and Pythonic way to manage database operations.
*   **Validation**: Pydantic is used for data validation to ensure the integrity of the data received by the API.

## Database Schema

The database consists of three tables:

*   **users**: Stores user information (id, email, hashed_password).
*   **chat_sessions**: Stores chat session information (id, user_id, created_at).
*   **messages**: Stores message information (id, text, created_at, session_id, user_id).

Relationships are defined as follows:
*   A user can have multiple chat sessions and messages.
*   A chat session belongs to one user and can have multiple messages.
*   A message belongs to one chat session and one user.

## Security Considerations

*   **Password Hashing**: Passwords are hashed using bcrypt before being stored in the database.
*   **JWT Security**: The `SECRET_KEY` used for signing JWTs should be kept secret and managed securely in a production environment (e.g., using environment variables).
*   **Input Validation**: All incoming data is validated using Pydantic to prevent common security vulnerabilities like injection attacks.

## Scalability Considerations

*   **Asynchronous DB Access**: The application is designed for async DB access, which can improve performance under high load. While SQLite's `aiosqlite` driver can be used, the current implementation uses a synchronous driver with `Depends` for simplicity in this example. For true async DB access, `databases` library or `SQLAlchemy`'s async support with `asyncpg` (for PostgreSQL) would be a better choice.
*   **Database Scaling**: For a larger scale application, switching from SQLite to a more scalable database like PostgreSQL or MySQL would be necessary.
*   **Stateless API**: The API is stateless, relying on JWTs for authentication, which allows for horizontal scaling by adding more application instances.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

---
### For Windows Users

**1. Open the Terminal**

Open PowerShell or Command Prompt. You can find it by searching in the Start Menu.

**2. Navigate to the Project Folder**

Use the `cd` command to go to the project's directory.
```sh
cd path\to\your\project-folder
```

**3. Create and Activate a Virtual Environment**

A virtual environment isolates the project's dependencies.
```powershell
# Create the environment
python -m venv venv

# Before activating, you may need to allow scripts to run in this terminal session.
# This is a common Windows security feature.
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate the environment
.\venv\Scripts\activate
```
You will know it's active when you see `(venv)` at the start of your terminal prompt.

**4. Install Dependencies**

Install all the required packages from the `requirements.txt` file.
```sh
pip install -r requirements.txt
```

**5. Run the Application**
```sh
uvicorn main:app --reload
```
**OR**
Start the development server using `uvicorn`.
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
Keep this terminal window open. Closing it will stop the server.

**And Access the Application**

Open your web browser and navigate to:
[**http://localhost:8000**](http://localhost:8000)

You will be automatically redirected to the interactive API documentation.

---

### For macOS and Linux Users

**1. Open the Terminal**

Open your preferred terminal application.

**2. Navigate to the Project Folder**

Use the `cd` command to go to the project's directory.
```sh
cd path/to/your/project-folder
```

**3. Create and Activate a Virtual Environment**
```sh
# Create the environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate
```
You will know it's active when you see `(venv)` at the start of your terminal prompt.

**4. Install Dependencies**

Install all the required packages.
```sh
pip install -r requirements.txt
```

**5. Run the Application**

Start the development server using `uvicorn`.
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
Keep this terminal window open. Closing it will stop the server.

**6. Access the Application**

Open your web browser and navigate to:
[**http://localhost:8000**](http://localhost:8000)

You will be automatically redirected to the interactive API documentation.

---

## Troubleshooting

### Error: "Address already in use"

This means another process is already using port 8000.

*   **On Windows:**
    1.  Find the process ID (PID): `netstat -ano | findstr :8000`
    2.  Stop the process: `taskkill /PID <PID> /F` (replace `<PID>` with the number you found).

*   **On macOS/Linux:**
    1.  Find the process ID (PID): `lsof -i :8000`
    2.  Stop the process: `kill -9 <PID>` (replace `<PID>` with the number you found).

### Error: 500 Internal Server Error when Creating a User

This was a known issue caused by a version incompatibility between the `passlib` and `bcrypt` libraries. The `requirements.txt` file in this project has been updated to force the use of a compatible version (`bcrypt<4.0`) to prevent this error from occurring. If you install dependencies manually, ensure you use a compatible version.