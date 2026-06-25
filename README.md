# Inventory Management API

A backend inventory management API built with **Django** and **Django REST Framework**.

At the moment, this project only includes the API layer. No frontend application is currently included.

---

## Features

- Product management (create, update, delete, list)
- Inventory stock tracking
- Stock adjustment
- Transaction history (incoming/outgoing stock)
- Category management
- Supplier management
- REST API with authentication
- Search and filtering for products
- Transaction logs for auditing

---

## Tech Stack

### Backend

- Django
- Django REST Framework
- PostgreSQL / SQLite
- Simple JWT Authentication

---

## Backend Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

## Environment Variables

Create a `.env` file in the backend directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

---

## API Documentation

The API is available at:

```text
http://localhost:8000/api/
```

### Products

- `GET /api/products/` — List all products
- `POST /api/products/` — Create a new product
- `GET /api/products/{id}/` — Retrieve a product
- `PUT /api/products/{id}/` — Update a product
- `DELETE /api/products/{id}/` — Delete a product

### Transactions

- `GET /api/transactions/` — List all inventory transactions

### Stock Management

- `POST /api/stock/adjust/` — Adjust product stock levels

---

## Project Status

This project is currently focused on providing a RESTful API for inventory management. Frontend applications and client interfaces are not included at this stage.

---

## License

MIT License