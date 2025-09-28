# 🛍️ E-Commerce API (Capstone Project)

A Django REST Framework–based e-commerce backend with user authentication, product management, cart/wishlist, and order handling.  
Built as part of the ALX Capstone Project.

---

## 🚀 Features
- **User Authentication** (JWT-based with `djangorestframework-simplejwt`)
- **User Profiles** (extended with `is_seller`, `is_customer`, plus address & phone)
- **Product Management**  
  - Sellers can create, update, and delete their products  
  - Customers can browse products (with search, filtering, pagination)
- **Categories** for organizing products
- **Orders** (sellers can view orders for their products)
- **Cart & Wishlist** for customers
- **Permissions**  
  - Sellers: Full CRUD on their own products  
  - Customers: Read-only for products, can manage carts & wishlist
- **API Documentation** with Swagger/OpenAPI (via `drf-yasg`)

---

## 🛠️ Tech Stack
- **Backend Framework:** Django, Django REST Framework (DRF)
- **Authentication:** JWT (`djangorestframework-simplejwt`)
- **Database:** PostgreSQL (with SQLite for local dev)
- **Deployment:** Render
- **Other:** drf-yasg for API docs

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/OdegiChristine/alx-capstone-e-commerce.git
cd capstone_e_commerce
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Environment variables
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```
### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create a superuser
```bash
python manage.py createsuperuser
```
### 7. Runserver
```bash
python manage.py runserver
```

## API Documentation
Once the server is running, Swagger/OpenAPI docs are available at: `http://127.0.0.1:8000/swagger/`

## 🧪 Running Tests
```bash
pytest
```

## ✨ Future Improvements
- Add payments integration(Stripe/Paypal, Mpesa)
- Product reviews & ratings
- Seller dashboards
- Email notifications