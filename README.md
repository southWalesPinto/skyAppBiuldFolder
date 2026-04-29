# SkyAppBiuld

Django web app for managing users, teams, projects, meetings, and messaging.

## Table of Contents

- Description
- Tech
- Prerequisites
- Setup
- Database
- Run (development)
- Tests
- Static files
- Features

## Description

A modular Django project that provides internal team and project management features including accounts, projects, meetings, messaging, teams, and audit logs.

## Tech

- Python 3.12
- Django (version used by the project)
- SQLite (default development DB)

## Prerequisites

- `python3.12`
- `pip` or `pipx`
- Optional: `virtualenv` or venv

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install Django and other deps manually.

## Database

Apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Username: AdminSuper

Password: AdminSuper

## Run (development)

Start the development server:

```bash
python manage.py runserver
```

## Tests

Run the test suite with:

```bash
python manage.py test
```

## Static files

Collect static files for deployment:

```bash
python manage.py collectstatic
```

## Features

- `accounts` — custom user and profile management
- `projects` — project models and views
- `meetings` — scheduling and participants
- `messaging` — conversations and messages
- `teams` — team membership and roles
- `audit` — action logs
