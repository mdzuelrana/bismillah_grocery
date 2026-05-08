# 🛒 Grocery E-Commerce Backend API

Professional full-stack grocery e-commerce backend built with Django REST Framework, JWT authentication, role-based access control, SSLCommerz payment integration, and production-ready architecture.

---


# 🚀 Features


## Authentication
- JWT Authentication
- Djoser Authentication
- User Registration
- Login with Username & Password
- Email Activation
- Password Reset
- Role-Based Authentication

---


# 👥 User Roles

- Admin
- Seller
- Customer

---


# 🛍️ E-Commerce Features


## Products
- Product CRUD
- Product Categories
- Product Reviews
- Product Wishlist


## Cart
- Add to Cart
- Remove from Cart
- Update Quantity


## Orders
- Place Order
- Order History
- Order Details
- Seller Orders


## Payments
- SSLCommerz Integration
- Payment Validation
- Payment History
- Payment Success/Fail Handling

---


# 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Djoser
- SSLCommerz
- Supabase PostgreSQL
- Vercel Deployment

---


# 📁 Project Structure

```bash
grocery/
│
├── users/
├── tasks/
├── cart/
├── order/
├── review/
├── payments/
│
├── grocery/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt


🔐 Authentication Endpoints
/auth/users/
/auth/jwt/create/
/auth/jwt/refresh/
/auth/users/me/


📦 Main API Endpoints
Products
/api/products/
/api/products/{id}/
Cart
/api/cart/
/api/cart/{id}/
Orders
/api/orders/
/api/orders/{id}/
Payments
/api/payment/pay/{order_id}/
/api/payment/history/
/api/payment/validate/


⚙️ Environment Variables

Create .env file:

SECRET_KEY=your_secret_key

DATABASE_URL=your_database_url

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password

SSLCOMMERZ_STORE_ID=testbox
SSLCOMMERZ_STORE_PASSWORD=qwerty

FRONTEND_URL=***
BASE_URL=https:***

🧪 Installation
Clone Repository
git clone <repo_url>
cd grocery
Create Virtual Environment
python -m venv venv
Windows
source venv/Scripts/activate
Linux/Mac
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Run Migrations
python manage.py makemigrations
python manage.py migrate
Create Superuser
python manage.py createsuperuser
Run Server
python manage.py runserver

🌐 Deployment
Backend Deployment
Vercel
Database
Supabase PostgreSQL

🔥 Swagger API Documentation
/swagger/

🧾 Payment Flow
Customer Checkout
        ↓
Create Order
        ↓
SSLCommerz Payment Gateway
        ↓
Payment Validation
        ↓
Order Paid

👨‍💻 Author

Developed by Md Zuel Rana


📄 License

This project is licensed under the MIT License.
