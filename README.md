# Task Management System API

A production-ready RESTful API for managing tasks with secure JWT authentication, built with FastAPI and SQLAlchemy.

## 📋 Table of Contents

- [Task Management System API](#task-management-system-api)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
  - [🛠 Technology Stack](#-technology-stack)
  - [📁 Project Structure](#-project-structure)
  - [💻 Installation](#-installation)
    - [Prerequisites](#prerequisites)
    - [Step 1: Clone the Repository](#step-1-clone-the-repository)
    - [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
- [install dependencies](#install-dependencies)
- [Step 4: Configure Environment Variables](#step-4-configure-environment-variables)
  - [🚀 Running the Application](#-running-the-application)
  - [Security Features](#security-features)
  - [🎯 Quick Start Commands](#-quick-start-commands)

## ✨ Features

- **User Authentication**
  - Secure user registration and login
  - JWT-based authentication with token expiry
  - Password hashing using bcrypt
  - Account activation/deactivation support

- **Task Management**
  - Create, read, update, and delete tasks
  - Automatic timestamping on task creation
  - Task status tracking (pending, in_progress, completed)
  - Search and filter capabilities
  - Pagination support for large datasets
  - User-specific task isolation

- **Scheduling & Notifications**
  - Future task scheduling with datetime support
  - Automatic notifications 1 hour and 1 day before scheduled tasks
  - Background scheduler for notification handling

- **Security**
  - JWT token validation on protected routes
  - Password strength validation
  - SQL injection protection via SQLAlchemy ORM
  - CORS middleware configuration

## 🛠 Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.104.1 | Web framework |
| SQLAlchemy | 2.0.23 | ORM for database operations |
| Pydantic | 2.5.0 | Data validation |
| PyJWT | 2.8.0 | JWT token handling |
| Passlib | 1.7.4 | Password hashing |
| bcrypt | 4.0.1 | Password hashing algorithm |
| APScheduler | 3.10.4 | Task scheduling for notifications |
| Uvicorn | 0.24.0 | ASGI server |
| PostgreSQL/SQLite | - | Database |

## 📁 Project Structure

task_management_system/

├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── common.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   └── notification_service.py
├── requirements.txt
├── .env
└── run.py



## 💻 Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL (optional, SQLite works for development)
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/task-management-system.git
cd task-management-system
```

### Step 2: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

# install dependencies
```bash
pip install -r requirements.txt
``` 
# Step 4: Configure Environment Variables
Create a `.env` file in the root directory and add the following variables:

```env  
# Database Configuration
DATABASE_URL=sqlite:///./tasks.db  # For development
# For production with PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/taskdb

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
## 🚀 Running the Application
```bash
python run.py
```

## Security Features
- **JWT Authentication**: All protected routes require a valid JWT token, which is generated upon successful login and includes an expiration time.
- **Password Hashing**: User passwords are securely hashed using bcrypt before being stored in the database, ensuring that plaintext passwords are never saved.
- **Input Validation**: Pydantic models are used to validate incoming data, preventing common security vulnerabilities such as SQL injection and ensuring data integrity.
- **CORS Middleware**: Configured to allow cross-origin requests from trusted domains, enhancing security while enabling frontend integration.

## 🎯 Quick Start Commands
```bash
# Clone and setup
git clone <repository-url>
cd task-management-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings

# Initialize database
python -c "from app.core.database import engine, Base; from app.models import user, task; Base.metadata.create_all(bind=engine)"

# Run
python run.py

# Access API docs
open http://localhost:8000/docs
```