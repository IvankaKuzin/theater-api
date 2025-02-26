# Theater API

A modern RESTful API for managing theater resources including performances, reservations, and user accounts.

## Overview

The Theater API provides a complete backend solution for theater management systems. It allows for managing theater performances, handling ticket reservations, and user authentication/authorization. Built with Django and Django REST Framework, it follows best practices for security, documentation, and API design.

## Features

- **User Management**: Registration, authentication, and profile management
- **Performance Management**: Create, read, update, and delete theater performances
- **Reservation System**: Book tickets and manage reservations
- **Admin Dashboard**: Administrative interface for theater management
- **API Documentation**: Comprehensive documentation with drf-spectacular
- **Permissions**: Role-based access control for different user types

## Technology Stack

- **Framework**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Django Test Framework

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/IvankaKuzin/theater-api.git
   cd theater-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file based on `.env.sample`
   - Set your database credentials and other configuration options

If you chose local settings file:
1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```
   
If you chose docker settings file:
1. Build and start the Docker containers:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

2. Apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access the API at http://localhost:8000/api/

## Environment Variables (.env file)

Make the following changes to your .env file:

```
# Database settings
POSTGRES_PASSWORD=your_database_password
POSTGRES_USER=your_database_user
POSTGRES_DB=theater_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data

# Django settings
DJANGO_SECRET_KEY=your_secure_secret_key
DJANGO_SETTINGS_MODULE=path_to_settings_file # Use theatre_service.settings.docker for Docker, theatre_service.settings.local for local development
```

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

## API Endpoints

### User Management
- `POST /api/user/register/` - Register a new user
- `POST /api/user/token/` - Obtain authentication tokens
- `GET/PUT/PATCH /api/user/me/` - Retrieve or update authenticated user profile

### Performances
- `GET /api/theater/performances/` - List all performances
- `POST /api/theater/performances/` - Create a new performance (admin only)
- `GET /api/theater/performances/{id}/` - Retrieve performance details
- `PUT/PATCH /api/theater/performances/{id}/` - Update a performance (admin only)
- `DELETE /api/theater/performances/{id}/` - Delete a performance (admin only)

### Genres
- `GET /api/theater/genres/` - List all genres
- `POST /api/theater/genres/` - Create a new genre (admin only)
- `GET /api/theater/genres/{id}/` - Retrieve genre details
- `PUT/PATCH /api/theater/genres/{id}/` - Update a genre (admin only)
- `DELETE /api/theater/genres/{id}/` - Delete a genre (admin only)

### Actors
- `GET /api/theater/actors/` - List all actors
- `POST /api/theater/actors/` - Add a new actor (admin only)
- `GET /api/theater/actors/{id}/` - Retrieve actor details
- `PUT/PATCH /api/theater/actors/{id}/` - Update actor information (admin only)
- `DELETE /api/theater/actors/{id}/` - Remove an actor (admin only)

### Plays
- `GET /api/theater/plays/` - List all plays
- `POST /api/theater/plays/` - Create a new play (admin only)
- `GET /api/theater/plays/{id}/` - Retrieve play details
- `PUT/PATCH /api/theater/plays/{id}/` - Update a play (admin only)
- `DELETE /api/theater/plays/{id}/` - Delete a play (admin only)

### Theatre Halls
- `GET /api/theater/theatre-halls/` - List all theatre halls
- `POST /api/theater/theatre-halls/` - Create a new theatre hall (admin only)
- `GET /api/theater/theatre-halls/{id}/` - Retrieve theatre hall details
- `PUT/PATCH /api/theater/theatre-halls/{id}/` - Update a theatre hall (admin only)
- `DELETE /api/theater/theatre-halls/{id}/` - Delete a theatre hall (admin only)

### Reservations
- `GET /api/theater/reservations/` - List user's reservations
- `POST /api/theater/reservations/` - Create a new reservation
- `GET /api/theater/reservations/{id}/` - Retrieve reservation details
- `DELETE /api/theater/reservations/{id}/` - Cancel a reservation

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contact
Project Link: [https://github.com/IvankaKuzin/theater-api](https://github.com/IvankaKuzin/theater-api)
