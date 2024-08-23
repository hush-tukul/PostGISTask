# Building & Deployment Guide

## Prerequisites

- **Version Control**: Ensure code is committed to the repository.
- **Dependencies**: List in `requirements.txt` or similar.
- **Access**: Necessary permissions for deployment.

## Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/hush-tukul/PostGISTask.git
    cd PostGISTask
    ```

2. **Create a Virtual Environment** (if working outside Docker):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Build and Run Docker Containers**:
    ```bash
    docker-compose up --build
    ```

## Database Setup

1. **Create Superuser**:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

2. **Make Migrations**:
    ```bash
    docker-compose exec web python geo_project/manage.py makemigrations
    ```

3. **Apply Migrations**:
    ```bash
    docker-compose exec web python geo_project/manage.py migrate
    ```

## Deployment

### Staging

1. **Deploy to Staging**:
    ```bash
    docker-compose up -d
    ```

### Production

1. **Deploy to Production**:
    ```bash
    docker-compose -f docker-compose.prod.yml up -d
    ```

## Rollback

1. **Rollback Deployment**:
    ```bash
    docker-compose down
    docker-compose -f docker-compose.prod.yml up -d
    ```

## Troubleshooting

- **Logs**: Check logs for errors.
  ```bash
  docker-compose logs
