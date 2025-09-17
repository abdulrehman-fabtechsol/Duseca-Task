# Internal Recruitment System

## Tech Stack

* Python 3.10.6
* PostgreSQL

> Minimum required versions to run this project.

---

## Docker Setup (Recommended)

### Prerequisites

* Install **Docker** and **docker-compose**.

### Steps

1. Clone the repository:

```bash
git clone <repo_url>
cd <repo_folder>
```

2. Create a `.env` file with the following environment variables:

```env
# Docker environment
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Local environment (used if not running in Docker)
LOCAL_DB_NAME=local_db
LOCAL_DB_USER=local_user
LOCAL_DB_PASSWORD=local_pass
LOCAL_DB_HOST=localhost
LOCAL_DB_PORT=5432
```

3. Build and start the containers:

```bash
docker-compose up --build
```

it will build container and also polate the 5 users and 5 books for sample





4. Access the application at [http://localhost:80]

---

5. Swagger apis are at url [http://localhost/openapi/]


Admin Credentials for Swager apis lock (after populate command in docker it populates automatic) 
email:        user1@example.com
password:     aszx1234


### Database Configuration in `settings.py`

```python
import os

IN_DOCKER = os.environ.get("DB_HOST") == "db"

if IN_DOCKER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('LOCAL_DB_NAME'),
            'USER': os.environ.get('LOCAL_DB_USER'),
            'PASSWORD': os.environ.get('LOCAL_DB_PASSWORD'),
            'HOST': os.environ.get('LOCAL_DB_HOST'),
            'PORT': os.environ.get('LOCAL_DB_PORT', '5432'),
        }
    }
```


just comment docker db env env if using not docker

---

## Without Docker Setup

### Python Setup

1. Clone the repository:

```bash
git clone <repo_url>
cd <repo_folder>
```

2. Install Python dependencies:

```bash
# Install pip if not installed: https://pip.pypa.io/en/stable/installation/
# Install virtualenv: https://virtualenv.pypa.io/en/latest/index.html
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

The application will be accessible at [http://localhost:8000](http://localhost:8000)

---

### Pre-Commit Hooks

To enforce project-wide code quality checks:

```bash
pre-commit install --hook-type pre-commit
```

---

### Populate Database

```bash
# Run migrations if needed
python manage.py migrate

# Flush database if needed
python manage.py flush

# Add fake data to database
python manage.py populate
```


### Schema Design Decisions


User

1. Custom user model using email as USERNAME_FIELD for login.

2. email is unique and required, name is optional.

3. Decision: Use email login instead of username for modern authentication practices.

Book

1. Stores title, author, published_date, isbn.

2. isbn is unique to prevent duplicates.

3. Decision: Keep core book metadata, enforce uniqueness on ISBN for integrity.

Review

1. Relates User ↔ Book via ForeignKey.

2. related_name set for easy reverse querying (book_reviews, user_reviews).

3. rating is constrained between 1–5 with choices for clarity.

4. unique_together ensures one review per user per book.

5. Decision: Maintain data integrity, enforce business rules at schema level.


### Schema Design image 
it is location in roat directory