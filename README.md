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


4. **Build and Run Docker Containers**:
    ```bash
    docker-compose up --build
    ```

## Database Setup

1. **Create Superuser**:
    ```bash
    docker-compose exec web python geo_project/manage.py createsuperuser
    ```
2. **Login in admin page**:
   ```bash
   http://localhost:8000/admin/login/
   ```

**Now you can use swagger page**:
      ```
      http://localhost:8000/swagger/
      ```


OPTIONAL
3. **Make Migrations**:
    ```bash
    docker-compose exec web python geo_project/manage.py makemigrations
    ```

4. **Apply Migrations**:
    ```bash
    docker-compose exec web python geo_project/manage.py migrate
    ```

## Deployment

### Staging

1. **Deploy to Staging**:
    ```bash
    docker-compose up -d
    ```

## Rollback

1. **Rollback Deployment**:
    ```bash
    docker-compose down
    ```

