```markdown
# Inventory Management System

A full-stack inventory management system built with **React + TypeScript** for the frontend and **Django + Django REST Framework** for the backend.  
The system allows businesses to manage products, stock levels, and inventory transactions with a clean web interface and a RESTful API.

---

## Features

- Product management (create, update, delete, list)
- Inventory stock tracking
- Stock adjustment
- Transaction history (incoming/outgoing stock)
- Category management
- Supplier management
- REST API with authentication
- Responsive frontend dashboard
- Search and filtering for products
- Transaction logs for auditing

---

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Axios
- React Router
- TailwindCSS

### Backend
- Django
- Django REST Framework
- PostgreSQL / SQLite
- Simple JWT authentication

---

## Backend Setup (Django)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
source venv/bin/activate   # Linux/Mac
```

Windows:

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

### 6. Run Server

```bash
python manage.py runserver
```

---

## Frontend Setup (React)

### 1. Navigate to Frontend

```bash
cd ../frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Server

```bash
npm run dev
```

---

## Environment Variables

Create `.env` file in the backend directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

---

## API Documentation

API endpoints are available at `http://localhost:8000/api/`

- `GET /api/products/` - List all products
- `POST /api/products/` - Create new product
- `GET /api/products/{id}/` - Get a product
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product
- `GET /api/transactions/` - List transactions
- `POST /api/stock/adjust/` - Adjust stock

---

## License

MIT License
```
