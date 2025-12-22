# Django ToDO List

## Description
This is an educational backend-focused project built to practice Django fundamentals.
The main goals are mastering Class-Based Views (CBV), implementing authentication, writing automated tests, and enforcing strict access control so users can work only with their own tasks.

## Notes
This project was created for learning purposes and focuses on backend architecture rather than UI design.

## Access Control
- Per-user data isolation (users can access only their own tasks)

## Features
- User authentication
- Task CRUD operations
- Task filtering by status (active / completed / all)
- Bulk task deletion
- Automated tests

## Tech Stack
- Language: Python 3.14
- Framework: Django 6.0
- Environment: django-environ
- Database: PostgreSQL

## Project Setup
1. Git Clone
```bash
git clone
cd django-todo-list
```
2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Setup database PostgreSQL
    - Create Database
    - Setup `.env` file, using `.env.example` in main directory
```dotenv
SECRET_KEY=secret_key

DB_NAME=db_name
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=db_host
DB_PORT=5432
```
5. Use migrations
```bash
python manage.py migrate
```
6. Create superuser
```bash
python manage.py createsuperuser
```
7. Run project
```bash
python manage.py runserver
```
The project will be available at: http://127.0.0.1:8000/

## Testing

To run the test suite, use the following command:
```bash
python manage.py test todo_list.tests
```