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
- TailwindCSS (optional)

### Backend
- Django
- Django REST Framework
- PostgreSQL / SQLite
- Simple JWT authentication

---

## Project Structure

```

inventory-system/
│
├── backend/
│   ├── inventory_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── asgi.py
│   │
│   ├── inventory/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts
│   │   │
│   │   ├── components/
│   │   │   ├── ProductTable.tsx
│   │   │   ├── StockCard.tsx
│   │   │   └── TransactionList.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Products.tsx
│   │   │   └── Transactions.tsx
│   │   │
│   │   ├── types/
│   │   │   └── inventory.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   └── tsconfig.json
│
└── README.md

````

---

# Backend Setup (Django)

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system/backend
````

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`

```
Django
djangorestframework
djangorestframework-simplejwt
django
```
