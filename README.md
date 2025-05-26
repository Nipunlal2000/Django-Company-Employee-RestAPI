# Django Company Employee API 🚀

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-4.x-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

A RESTful API built with Django and Django REST Framework to manage companies and their employees with secure JWT-based authentication, custom user model, and robust password management (change/reset).

---

## 🔑 Features

- ✅ Custom **User model** (`Company`) with email-based login.
- ✅ JWT **Authentication** using `SimpleJWT`.
- ✅ Full **CRUD operations** for Employee model.
- ✅ Company-based employee filtering (users only see their employees).
- ✅ Password **Change** (with old password verification).
- ✅ Password **Reset** (with email token & confirmation flow).
- ✅ Django Admin support for managing companies and employees.
- ✅ Token Refresh & Blacklist functionality for secure session handling.

---

## 🧩 Tech Stack

- **Python 3.9+**
- **Django 4.x**
- **Django REST Framework**
- **Simple JWT**
- **SQLite** (default, easily swappable)
- **Pillow** (for image upload support)

---

## 🔧 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/django-company-employee-api.git
   cd django-company-employee-api

2. **Create a virtual environment & activate** <br>
   ``python -m venv venv
  source venv/bin/activate  # Windows: venv\Scripts\activate
  ``
3. **Install dependencies** <br>
   `` pip install -r requirements.txt
  ``
4. **Apply migrations** <br>
   ``python manage.py makemigrations
    python manage.py migrate ``
   
5. **Create a superuser** <br>
   ``python manage.py createsuperuser ``
   
7. **Run the development server** <br>
   ``python manage.py runserver``

### 📦 API Endpoints
| Endpoint                                        | Method | Description                              |
| ----------------------------------------------- | ------ | ---------------------------------------- |
| `/api/register/`                                | POST   | Register a new company user              |
| `/api/login/`                                   | POST   | Obtain JWT access & refresh tokens       |
| `/api/refresh/`                                 | POST   | Refresh token                            |
| `/api/employees/`                               | GET    | List all employees for logged-in company |
| `/api/employees/`                               | POST   | Create a new employee (linked to user)   |
| `/api/employees/<id>/`                          | GET    | Retrieve employee by ID                  |
| `/api/employees/<id>/`                          | PATCH  | Update employee info                     |
| `/api/employees/<id>/`                          | DELETE | Delete employee                          |
| `/api/change-password/`                         | POST   | Change password (old required)           |
| `/api/request-reset-password/`                  | POST   | Send password reset email                |
| `/api/password-reset-confirm/<uidb64>/<token>/` | POST   | Reset password with new/confirm          |


