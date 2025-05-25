# **E-Commerce API**

A production-ready RESTful API for a simple e-commerce platform. This project leverages **FastAPI** for API development, supports testing with **pytest**, and uses **Docker** for containerized deployment including a PostgreSQL database.

---

## **Getting Started**

### Prerequisites
- Docker installed on your machine.
- uv with Python 3.10+ (optional for local development).

---

### **Running the Application**

#### **Using Docker Compose**
1. Build and start the services:
   ```bash
   docker-compose up --build app
   ```

2. Access the backend application:
   - API-DOCS: [Swagger](http://localhost:8000/docs)
   - Health Check: [http://localhost:8000/health](http://localhost:8000/health)

#### **Running Locally**
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Do migrations if needed:
   ```bash
   uv run alembic upgrade head
   ```

3. Run the application:
   ```bash
   uv run fastapi run app/main.py --host 0.0.0.0 --port 8000
   ```

---

### **Running Tests**

#### **With Docker**
1. Run the test container:
   ```bash
   docker-compose up pytest
   ```

#### **Locally**
1. Install test dependencies:
   ```bash
   uv sync
   ```

2. Run the tests:
   ```bash
   uv run pytest -vvv
   ```

---

## **Endpoints**

| Method | Endpoint        | Description           |
|--------|-----------------|-----------------------|
| GET    | `/products`     | Retrieve all products |
| POST   | `/products`     | Add a new product     |
| GET    | `/orders`       | Retrieve all orders   |
| POST   | `/orders`       | Place an order        |
| GET    | `/health`       | Health check endpoint |

---
