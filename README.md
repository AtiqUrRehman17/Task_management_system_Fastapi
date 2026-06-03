# Task Management System API

A production-ready RESTful Task Management API built with FastAPI, SQLAlchemy, JWT Authentication, Redis, and Celery. The system supports user authentication, task management, scheduling, and asynchronous background notifications.

---

# 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Architecture](#architecture)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Running the Application](#running-the-application)
* [Running Redis](#running-redis)
* [Running Celery Worker](#running-celery-worker)
* [API Documentation](#api-documentation)
* [Notification Workflow](#notification-workflow)
* [Testing Notifications](#testing-notifications)
* [Security Features](#security-features)
* [Future Improvements](#future-improvements)

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

---

# Features

## User Authentication

* User Registration
* User Login
* JWT Token Authentication
* Password Hashing with bcrypt
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
| SQLite / PostgreSQL | Database                   |
| Pydantic            | Validation                 |
| JWT                 | Authentication             |
| Passlib + bcrypt    | Password Hashing           |
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

```text
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
```

### Benefits

* Production-ready
* Persistent scheduling
* Supports multiple workers
* Scalable architecture
* Distributed task processing

---

# Project Structure

```text
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
cd task-management-system
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv myenv
myenv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./tasks.db

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

# Running the Application

## Start FastAPI

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

Expected Output:

```text
Uvicorn running on http://0.0.0.0:8000
```

---

# Running Redis

## Using Docker

```bash
docker run -d --name redis -p 6379:6379 redis
```

Start existing container:

```bash
docker start redis
```

Verify:

```bash
docker ps
```

---

# Running Celery Worker

Open a separate terminal:

### Windows

```bash
celery -A app.celery_app:celery_app worker --pool=solo --loglevel=info
```

Expected Output:

```text
[tasks]
 . app.workers.notification_tasks.send_notification
```

This confirms the worker has successfully registered the notification task.

---

# API Documentation

After starting the application:

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Notification Workflow

## Task Creation

When a task is created:

```text
User
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

---

## Task Update

When a scheduled task is updated:

```text
Existing notifications cancelled
          │
          ▼
New notifications scheduled
          │
          ▼
Stored again in Redis
```

---

## Task Deletion

When a task is deleted:

```text
Delete Task
      │
      ▼
Revoke Celery Notifications
      │
      ▼
Remove Task from Database
```

---

# Testing Notifications

## Step 1

Start Redis.

---

## Step 2

Start FastAPI.

---

## Step 3

Start Celery Worker.

---

## Step 4

Login and obtain JWT token.

---

## Step 5

Authorize in Swagger UI.

---

## Step 6

Create a task with a future scheduled time.

Example:

```json
{
  "title": "Test Notification",
  "description": "Testing Celery",
  "status": "pending",
  "scheduled_time": "2026-12-31T23:00:00Z"
}
```

---

## Step 7

Observe Celery Worker logs.

Expected:

```text
Task received
Notification sent to user@example.com
```

---

## Quick Testing Tip

For faster testing:

Temporarily replace:

```python
timedelta(days=1)
timedelta(hours=1)
```

with:

```python
timedelta(minutes=2)
timedelta(minutes=1)
```

Then create a task scheduled a few minutes in the future.

---

# Security Features

## JWT Authentication

* Secure access tokens
* Expiration support
* Protected routes

## Password Hashing

* bcrypt hashing
* Plain-text passwords never stored

## Input Validation

* Pydantic schema validation
* Type-safe request handling

## ORM Security

* SQLAlchemy ORM
* Protection against SQL injection

## CORS Support

Configurable CORS middleware for frontend integration.

---

# Future Improvements

## Email Notifications

* SMTP Integration
* Gmail SMTP
* SendGrid
* Amazon SES

## Retry Mechanism

Automatic retry for failed notifications.

## Alembic Migrations

Database versioning and schema migrations.

## Docker Deployment

Containerized FastAPI, Redis, and Celery setup.

## Monitoring

* Flower Dashboard
* Celery Monitoring
* Redis Monitoring

## WebSocket Notifications

Real-time browser notifications.

---

# Quick Start

```bash
# Clone project
git clone <repository-url>

# Enter directory
cd task-management-system

# Create environment
python -m venv myenv

# Activate environment
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis
docker start redis

# Terminal 1
python run.py

# Terminal 2
celery -A app.celery_app:celery_app worker --pool=solo --loglevel=info

# Open Swagger
http://localhost:8000/docs
```

---

# Author

Task Management System API built using FastAPI, SQLAlchemy, Redis, and Celery following scalable backend development practices.
