# FastAPI CRUD Boilerplate

A production-ready FastAPI boilerplate with async SQLAlchemy, Pydantic v2, and Docker. This template provides a solid foundation for building scalable RESTful APIs with best practices in mind.

## Features

- **FastAPI** for high-performance API development
- **Async SQLAlchemy 2.0** with PostgreSQL support
- **Pydantic v2** for data validation
- **Docker** and **Docker Compose** ready
- **Unit & Integration Tests** with pytest
- **Testing** with pytest-asyncio

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- UV package manager (recommended)

### Running with Docker (Recommended)


1. Clone the repository:
   ```bash
   git clone https://github.com/ahdhani/boilerplate.git
   cd boilerplate
   ```

2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

3. Start the services:
   ```bash
   docker-compose up --build app
   ```

4. Access the application:
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health


## Running Tests

Run tests using Docker:
```bash
docker-compose up pytest
```

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
