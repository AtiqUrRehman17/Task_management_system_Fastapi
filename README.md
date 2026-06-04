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
    - [Benefits:](#benefits)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
  - [Clone Repository](#clone-repository)
    - [Using Docker](#using-docker)
  - [Start existing container:](#start-existing-container)
  - [Running Celery Worker](#running-celery-worker)
  - [API Documentation](#api-documentation)
  - [Notification Workflow](#notification-workflow)
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
  - [Security Features](#security-features)
    - [JWT Authentication](#jwt-authentication)
  - [Password Hashing](#password-hashing)
  - [Input Validation](#input-validation)
  - [ORM Security](#orm-security)
  - [Database Migrations](#database-migrations-1)
  - [Recent Changes](#recent-changes)
  - [User Model Updates](#user-model-updates)
  - [JWT Token Payload Updates](#jwt-token-payload-updates)
  - [Password Hashing Updates](#password-hashing-updates)
  - [Database Migration](#database-migration)
  - [Requirements Updates](#requirements-updates)
      - [Task Management System API built using FastAPI, SQLAlchemy, Redis, Celery, and Alembic following scalable backend development practices.](#task-management-system-api-built-using-fastapi-sqlalchemy-redis-celery-and-alembic-following-scalable-backend-development-practices)

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
## Limitations
- In-memory scheduling
- Jobs lost on restart
- Not suitable for multiple workers
- Difficult to scale horizontally

## Current Architecture (Redis + Celery)

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

Notification Task

### Benefits:
- Production-ready
- Persistent scheduling
- Supports multiple workers
- Scalable architecture
- Distributed task processing

## Project Structure

task_management_system/

├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── celery_app.py
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
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini
├── requirements.txt
├── .env
├── run.py
└── tasks.db

## Installation
### Prerequisites

Python 3.10+

Redis

Git

Virtual Environment

## Clone Repository
```bash
git clone <repository-url>
```

```bash
cd task_management_system
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```

```bashalembic upgrade head
```

```bashuvicorn app.main:app --reload
```

```bashcelery -A app.celery_app worker --loglevel=info
```
### Using Docker

```docker run -d --name redis -p 6379:6379 redis
```
## Start existing container:

```docker start redis
```

## Running Celery Worker
Windows
```bashcelery -A app.celery_app worker --loglevel=info
```
Linux/Mac
```bashcelery -A app.celery_app worker --loglevel=info
```
## API Documentation
Once the FastAPI server is running, you can access the interactive API documentation at:

```http://localhost:8000/docs
```

## Notification Workflow
```User
  │
  ▼
POST /tasks
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
```Existing notifications cancelled
          │
          ▼
New notifications scheduled
          │
          ▼
Stored again in Redis
```
## Task Deletion
```Delete Task
      │
      ▼
Revoke Celery Notifications
      │
      ▼
Remove Task from Database
```

## Testing Notifications
## Step 1
Start Redis.

## Step 2
Start FastAPI.

## Step 3
Start Celery Worker.

## Step 4
Login and obtain JWT token.

## Step 5
Authorize in Swagger UI.

## Step 6
Create a task with a future scheduled time.

example
```{
  "title": "Test Notification",
  "description": "Testing Celery",
  "status": "pending",
  "scheduled_time": "2026-12-31T23:00:00Z"
}
```

## Step 7
Expected:
```Task received
Notification sent to user@example.com
```
## Security Features
### JWT Authentication
- Secure access tokens
- Expiration support
- Protected routes
- Token payload includes ID, First Name, - - Last Name, Username, and Email

## Password Hashing
- Direct bcrypt hashing (no passlib dependency)
- Plain-text passwords never stored
- Maximum password length validation (72 bytes bcrypt limit)

## Input Validation
- Pydantic schema validation
- Type-safe request handling
- Password must contain uppercase, lowercase, and digit

## ORM Security
- SQLAlchemy ORM
- Protection against SQL injection
  
## Database Migrations
Alembic is used for database schema versioning and migrations.

Setup (Already Done):
Alembic is already initialized in this project. No setup needed.

## Recent Changes
## User Model Updates
- Added first_name field (Optional)
- Added last_name field (Optional)

## JWT Token Payload Updates
- Token now includes first_name and last_name
- Token now includes user id as sub

## Password Hashing Updates
- Removed passlib dependency completely
- Now using bcrypt directly for password hashing and verification
## Database Migration
- Alembic integrated for safe schema migrations
- Initial migration created for users and tasks tables

## Requirements Updates
- Removed passlib
- Added alembic
- bcrypt used directly

#### Task Management System API built using FastAPI, SQLAlchemy, Redis, Celery, and Alembic following scalable backend development practices.