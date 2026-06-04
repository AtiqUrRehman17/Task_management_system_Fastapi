# Task Management System API

A production-ready RESTful Task Management API built with FastAPI, SQLAlchemy, JWT Authentication, Redis, Celery, and Alembic. The system supports user authentication, task management, scheduling, and asynchronous background notifications.

---

# 📋 Table of Contents

- [Task Management System API](#task-management-system-api)
- [📋 Table of Contents](#-table-of-contents)
- [Overview](#overview)
- [Features](#features)
  - [User Authentication](#user-authentication)
  - [Task Management](#task-management)
  - [Task Scheduling \& Notifications](#task-scheduling--notifications)
  - [Database Migrations](#database-migrations)
  - [Production-Ready Architecture](#production-ready-architecture)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
  - [Previous Architecture (APScheduler)](#previous-architecture-apscheduler)
    - [Limitations](#limitations)
  - [Current Architecture (Redis + Celery)](#current-architecture-redis--celery)
  - [Notification Task](#notification-task)
    - [Benefits](#benefits)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone Repository](#clone-repository)
  - [Create Virtual Environment and Install Dependencies](#create-virtual-environment-and-install-dependencies)
    - [Using Docker](#using-docker)
  - [Start existing container:](#start-existing-container)
  - [Running Celery Worker](#running-celery-worker)
  - [Apply Database Migrations](#apply-database-migrations)
  - [API Documentation](#api-documentation)
  - [Notification Workflow](#notification-workflow)
    - [Task Creation](#task-creation)
  - [Task Update](#task-update)
  - [Task Deletion](#task-deletion)
  - [Testing Notifications](#testing-notifications)
  - [Step 1](#step-1)
  - [Step 2](#step-2)
  - [Step 3](#step-3)
  - [Step 4](#step-4)
  - [Step 5](#step-5)
  - [Step 6](#step-6)
  - [Step 7](#step-7)
  - [Step 8](#step-8)
  - [Security Features](#security-features)
  - [JWT Authentication](#jwt-authentication)
  - [Password Hashing](#password-hashing)
  - [Input Validation](#input-validation)
  - [Response Consistency](#response-consistency)
  - [ORM Security](#orm-security)
  - [CORS Support](#cors-support)
  - [Database Migrations](#database-migrations-1)
  - [Recent Changes](#recent-changes)
  - [Auth Endpoint Path Update](#auth-endpoint-path-update)
  - [Response Consistency Update](#response-consistency-update)
  - [Task Statistics Response Update](#task-statistics-response-update)
  - [Configuration Update](#configuration-update)
  - [User Model Updates](#user-model-updates)
  - [JWT Token Payload Updates](#jwt-token-payload-updates)
  - [Password Hashing Updates](#password-hashing-updates)
  - [Database Migration Updates](#database-migration-updates)
  - [Author](#author)

---

# Overview

The Task Management System API allows authenticated users to manage their tasks efficiently. Users can create, update, retrieve, and delete tasks while also scheduling future reminders.

The application follows a layered architecture:

* FastAPI for API endpoints
* SQLAlchemy ORM for database operations
* JWT Authentication for security
* Redis as the message broker
* Celery for asynchronous background task execution
* SQLite/PostgreSQL for persistent storage
* Alembic for database migrations and schema versioning

---

# Features

## User Authentication

* User Registration with First Name and Last Name
* User Login
* JWT Token Authentication
* JWT Token Payload includes ID, First Name, Last Name, Username, and Email
* Password Hashing with bcrypt (direct, no passlib)
* Protected API Routes

## Task Management

* Create Tasks
* Retrieve Tasks
* Update Tasks
* Delete Tasks
* Task Status Tracking
* Pagination Support
* Search Support
* Sorting Support
* User-specific Task Isolation
* Task Statistics Summary

## Task Scheduling & Notifications

* Future Task Scheduling
* Reminder Notifications
* Asynchronous Background Processing
* Celery-based Delayed Task Execution
* Redis-backed Message Queue
* Notification Cancellation on Task Updates
* Notification Rescheduling

## Database Migrations

* Alembic Integration
* Auto-generate Migrations from Models
* Safe Schema Updates without Data Loss
* Migration History Tracking
* Rollback Support

## Production-Ready Architecture

* Distributed Task Queue
* Multi-worker Support
* Horizontal Scaling Support
* Separation of API and Background Processing
* Redis-backed Scheduling

---

# Technology Stack

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| FastAPI             | Web Framework              |
| SQLAlchemy          | ORM                        |
| Alembic             | Database Migrations        |
| SQLite / PostgreSQL | Database                   |
| Pydantic            | Validation                 |
| JWT                 | Authentication             |
| bcrypt              | Password Hashing           |
| Redis               | Message Broker             |
| Celery              | Background Task Processing |
| Uvicorn             | ASGI Server                |

---

# Architecture

## Previous Architecture (APScheduler)

```text
FastAPI
   │
   ▼
NotificationService
   │
   ▼
APScheduler
   │
   ▼
Notification Function

```

### Limitations

* In-memory scheduling
* Jobs lost on restart
* Not suitable for multiple workers
* Difficult to scale horizontally

---

## Current Architecture (Redis + Celery)

```
FastAPI
   │
   ▼

TaskService
   │
   ▼

NotificationService
   │
   ▼

Redis Broker
   │
   ▼

Celery Worker
   │
   ▼
   ```

## Notification Task

### Benefits

* Production-ready
* Persistent scheduling
* Supports multiple workers
* Scalable architecture
* Distributed task processing

---

# Project Structure

```
task_management_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── celery_app.py
├── pagination/
│   ├── __init__.py
│   ├── pagination.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── task.py
│   │   └── common.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── task_service.py
│   │   └── notification_service.py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   └── notification_tasks.py
│   │
│   └── utils/
│       └── response.py
│
├── alembic/
│   ├── versions/
│   │   └── 30918620af05_initial_migration.py
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── requirements.txt
├── .env
├── run.py
└── tasks.db
```

---

# Installation

## Prerequisites

* Python 3.10+
* Redis
* Git
* Virtual Environment

---

## Clone Repository

```bash
git clone <repository-url>
cd task_management_system
```
## Create Virtual Environment and Install Dependencies

```
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```

``` 
bashalembic upgrade head
```

```bash
uvicorn app.main:app --reload
```

```bash
celery -A app.celery_app worker --loglevel=info
```
### Using Docker

```
docker run -d --name redis -p 6379:6379 redis
```
## Start existing container:

```
docker start redis
```

## Running Celery Worker
Windows
```bash
celery -A app.celery_app worker --loglevel=info
```
Linux/Mac
```bash
celery -A app.celery_app worker --loglevel=info
```

## Apply Database Migrations

```
bash
alembic upgrade head
```
## API Documentation
After starting the application, access the interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
This documentation provides a user-friendly interface to explore and test all available API endpoints, including authentication, task management, and scheduling features.

## Notification Workflow
### Task Creation
```
User
  │
  ▼
POST /api/v1/tasks/
  │
  ▼
Task saved in database
  │
  ▼
NotificationService
  │
  ▼
Celery task scheduled
  │
  ▼
Task stored in Redis
```

## Task Update
```
Existing notifications cancelled
          │
          ▼
New notifications scheduled
          │
          ▼
Stored again in Redis
```
## Task Deletion
```
Delete Task
      │
      ▼
Revoke Celery Notifications
      │
      ▼
Remove Task from Database
```
## Testing Notifications

## Step 1
Start Redis:
```
docker start redis
```
## Step 2
Start FastAPI application:
```bash
uvicorn app.main:app --reload
```
or 
```
bash
python run.py
```

## Step 3
Start Celery Worker:

```bash
celery -A app.celery_app worker --loglevel=info
``` 
## Step 4
Register a new user at:
```
POST /api/v1/auth/register
```
## Step 5
Login and obtain JWT token at:
```
POST /api/v1/auth/login
```
## Step 6
```
Authorize in Swagger UI using the JWT token.
```
## Step 7
Create a task:

```
POST /api/v1/tasks/
```
```
eg
{
  "title": "Test Notification",
  "description": "Testing Celery",
  "status": "pending"
}
```
## Step 8
Observe Celery Worker logs

Expected Output:

```
Task received
Notification sent to user@example.com
```
## Security Features

## JWT Authentication
- Secure access tokens
- Expiration support
- Protected routes
- Token payload includes ID, First Name, Last Name, Username, and Email
- pydantic-settings handles SECRET_KEY loading (no os.getenv mixing)
- App fails immediately at startup if SECRET_KEY is missing

## Password Hashing
- Direct bcrypt hashing (no passlib dependency)
- Plain-text passwords never stored
- Maximum password length validation (72 bytes bcrypt limit)

## Input Validation
- Pydantic schema validation
- Type-safe request handling
- Password must contain at least one uppercase letter, one lowercase letter, and one digit

## Response Consistency
- All endpoints use api_response() from utils/response.py
- Task statistics use TaskStatisticsResponse Pydantic schema for validated responses
- No plain dict responses

## ORM Security
- SQLAlchemy ORM
- Protection against SQL injection
  
## CORS Support
- Configurable CORS middleware for frontend integration

## Database Migrations
Alembic is used for database schema versioning and migrations.

Note: Alembic is already initialized in this project. No setup needed.

## Recent Changes
## Auth Endpoint Path Update
- Register path changed from /api/v1/users/register to /api/v1/auth/register
- Login path changed from /api/v1/users/login to /api/v1/auth/login
- Both endpoints now grouped under Auth tag in Swagger UI

## Response Consistency Update
- Removed unused ResponseModel from schemas/common.py
- Deleted schemas/common.py entirely
- All endpoints consistently use api_response() from utils/response.py

## Task Statistics Response Update
- get_tasks_statistics() no longer returns a plain dict
- Added TaskStatisticsResponse Pydantic schema in schemas/task.py
- Statistics endpoint now returns validated Pydantic response
  
## Configuration Update
- Removed os.getenv("SECRET_KEY") from config.py
- Removed import os from config.py
- SECRET_KEY is now handled entirely by pydantic-settings
- App fails immediately at startup if SECRET_KEY is missing in .env

## User Model Updates
- Added first_name field (Optional)
- Added last_name field (Optional)

## JWT Token Payload Updates
- Token now includes first_name and last_name
- Token now includes user id as sub
## Password Hashing Updates
- Removed passlib dependency completely
- Now using bcrypt directly for password hashing and verification
## Database Migration Updates
- Alembic integrated for safe schema migrations
- Initial migration created for users and tasks tables
## Author

Task Management System API built using FastAPI, SQLAlchemy, Redis, Celery, and Alembic following scalable backend development practices.