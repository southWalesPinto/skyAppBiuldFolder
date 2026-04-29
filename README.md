# SkyAppBuild

Django web app for managing users, teams, projects, meetings, and messaging.

## Who built what (Group Contributions)

| Student | Contribution |
|--------|--------------|
| Thomas Mifsud | Accounts system, authentication, user profiles, database structure integration, backend coordination |
| Janefa Jeba | Messaging system (conversation, inbox, sent, drafts, compose message) |
| Mulugeta Zerufael | Scheduling system (meetings, calendar views, meeting management) |
| Rehan Sohail | Reports system (PDF/Excel generation and reporting features) +  Audit Log|

## Description

- Browse and search all engineering teams, and filters by name or department  
- View full team details including members, roles, skills, repositories and dependencies  
- Send messages through a built-in inbox system (inbox, sent, drafts)  
- Schedule meetings using monthly and weekly calendar views  
- View organisation structure showing departments and team relationships  
- Generate reports and download them as PDF or Excel files  
- Register accounts, log in, update profiles, and manage passwords  
- Admin panel for a full system management 

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

### Superuser Details

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
## Run migrations

```bash
python manage.py migrate
```
## Load sample data - messaging 
```bash
python3 manage.py loaddata data.json
```

## Features

- `accounts` — custom user and profile management
- `projects` — project models and views
- `meetings` — scheduling and participants
- `messaging` — conversations and messages
- `teams` — team membership and roles
- `audit` — action logs
