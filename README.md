Here’s a comprehensive `README.md` to document everything we did for your Django project using Vercel Postgres. This file includes setup instructions, configurations, and usage guidelines.

---

# Django Project with Vercel Postgres

This project is a Django application connected to a live Vercel Postgres database. It includes user registration, login, account activation, password reset functionality, and user profile access. 

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Endpoints](#endpoints)
- [Running Migrations](#running-migrations)
- [Usage](#usage)
- [Environment Variables](#environment-variables)

---

## Features

- **User Authentication**: Register, login, and activate accounts.
- **Password Reset**: Request and confirm password resets.
- **JWT Authentication**: Access token-based authentication for secure endpoints.
- **Profile Management**: Retrieve authenticated user profile details.
- **Live Database**: Powered by Vercel Postgres.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install PostgreSQL Driver**:
    ```bash
    pip install psycopg2-binary dj-database-url django-environ
    ```

## Configuration

### Step 1: Configure Django to Use Environment Variables

Add a `.env` file to store sensitive credentials like database credentials, secret keys, etc.

1. Create a `.env` file in the root directory:

    ```plaintext
    SECRET_KEY=your_secret_key
    DEBUG=True
    VERCEL_DB_NAME=verceldb
    VERCEL_DB_USER=default
    VERCEL_DB_PASSWORD=sYtLB4Nea6TA
    VERCEL_DB_HOST=ep-winter-snow-a41i3fbb.us-east-1.aws.neon.tech
    VERCEL_DB_PORT=5432
    ```

2. **Load Environment Variables**:
   Modify `settings.py` to load environment variables using `django-environ`.

    ```python
    import environ

    env = environ.Env()
    environ.Env.read_env()  # Loads .env file
    ```

### Step 2: Configure the Database in `settings.py`

Update `DATABASES` in `settings.py` to use Vercel Postgres.

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse("postgres://default:sYtLB4Nea6TA@ep-winter-snow-a41i3fbb.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require")
}
```

### Step 3: Configure JWT Authentication

Add JWT authentication with SimpleJWT in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Step 4: Set Up Email

Configure Django’s email backend in `settings.py` to enable email-based account activation and password reset:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
SITE_URL = 'http://127.0.0.1:8000'
```

## Database Setup

**Run Migrations**:
To set up database tables on the live database:

```bash
python manage.py migrate
```

**Create a Superuser** (optional):
```bash
python manage.py createsuperuser
```

## Endpoints

### Authentication Endpoints
- **Register**: `/api/register/`
- **Activate Account**: `/api/activate/<uidb64>/<token>/`
- **Login**: `/api/token/`
- **Password Reset Request**: `/api/password-reset/`
- **Password Reset Confirm**: `/api/password-reset-confirm/<uidb64>/<token>/`

### Profile Management
- **Get Profile**: `/api/profile/` (requires authentication)

## Usage

### Running the Development Server
To run the Django development server:

```bash
python manage.py runserver
```

### Testing Endpoints

1. **Register**: Use `/api/register/` to create a new user.
2. **Activate Account**: After registration, an activation email is sent to the user. Follow the link in the email to activate the account.
3. **Login**: Obtain a JWT token by sending a POST request to `/api/token/` with valid login credentials.
4. **Get Profile**: Use the token from the login response to access `/api/profile/`.

### Accessing Database Data on Vercel

You can use tools like `pgAdmin`, `DBeaver`, or `psql` to connect to Vercel Postgres and view or manage your data.

```bash
psql "postgres://default:sYtLB4Nea6TA@ep-winter-snow-a41i3fbb.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
```

## Environment Variables

| Variable           | Description                               |
|--------------------|-------------------------------------------|
| `SECRET_KEY`       | Django secret key                         |
| `DEBUG`            | Debug mode (True/False)                  |
| `VERCEL_DB_NAME`   | Database name for Vercel Postgres         |
| `VERCEL_DB_USER`   | Database user                             |
| `VERCEL_DB_PASSWORD` | Database password                       |
| `VERCEL_DB_HOST`   | Database host                             |
| `VERCEL_DB_PORT`   | Database port                             |
| `EMAIL_HOST_USER`  | SMTP email username                       |
| `EMAIL_HOST_PASSWORD` | SMTP email password                   |

This README provides a full guide for setting up, deploying, and using the Django app with Vercel Postgres. Let me know if you’d like further customization or additional details!