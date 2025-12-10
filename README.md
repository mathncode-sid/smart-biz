# SmartBiz - Sales Management Platform for Small Businesses

A simple, affordable sales and inventory management platform designed specifically for small and micro-businesses in Africa. Track inventory, record sales, and understand your business with real-time analytics—all at a price that makes sense for your budget.

## Overview

SmartBiz solves a critical problem: most business management tools are built for enterprises and priced accordingly. Small business owners, traders, and micro-entrepreneurs are left with spreadsheets, notebooks, or expensive solutions they can't afford. SmartBiz changes that.

Built with small businesses in mind, SmartBiz offers:
- Intuitive inventory tracking with low-stock alerts
- Real-time sales recording and revenue tracking
- Simple but powerful analytics
- Affordable subscription plans in KES
- Mobile-responsive design for on-the-go access

## Features

### Core Features
- **Product Management** - Add, edit, and delete products with buying and selling prices
- **Sales Tracking** - Record sales instantly and track revenue in real-time
- **Inventory Management** - Monitor stock levels and receive automatic low-stock alerts
- **Sales History** - View complete transaction history with timestamps and totals
- **Real-time Dashboard** - See key metrics at a glance: daily sales, product count, and low-stock items
- **7-Day Activity Chart** - Visual representation of sales trends over the past week

### Subscription System
- **Free Plan** - Up to 50 products, basic sales tracking, email support
- **Basic Plan (KES 499/month)** - Up to 500 products, advanced tracking, real-time analytics, priority support
- **Premium Plan (KES 1,499/month)** - Unlimited products, advanced reports, custom alerts, API access, 24/7 support

### Admin Dashboard
- Manage business owner accounts
- Monitor all subscriptions and due renewals
- Track total platform revenue
- Activate or deactivate user accounts
- View subscription status and details

### User Experience
- Clean, modern interface with no unnecessary complexity
- Mobile-responsive design works on phones, tablets, and desktops
- Fast performance optimized for low-bandwidth environments
- Role-based access control (admin vs regular users)
- Secure authentication and data protection

## Technology Stack

- **Backend** - Django 6.0, Python 3.12
- **Frontend** - HTML5, CSS3, Bootstrap 5.3.3, JavaScript
- **Database** - SQLite (development) / PostgreSQL (production-ready)
- **Styling** - Bootstrap 5, Google Fonts (Inter, Poppins)
- **Authentication** - Django built-in auth system with custom decorators
- **Deployment** - WSGI-compatible (Gunicorn, uWSGI)

## Project Structure

```
smart-biz/
├── smartbiz/                    # Main Django project
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── core/                        # Main application
│   ├── models.py               # Database models (User, Product, Sale, Subscription, SubscriptionPlan)
│   ├── views.py                # View logic (dashboard, products, sales, subscriptions, admin)
│   ├── utils.py                # Decorators (@subscription_required, @admin_required)
│   ├── context_processors.py   # Global context for templates
│   ├── management/
│   │   └── commands/
│   │       └── create_subscription_plans.py  # Management command for seeding plans
│   └── migrations/             # Database migrations
├── templates/
│   └── core/
│       ├── base.html                       # User dashboard base template
│       ├── admin_base.html                 # Admin dashboard base template
│       ├── landing.html                    # Public landing page
│       ├── login.html                      # Login page
│       ├── register.html                   # Registration page
│       ├── dashboard.html                  # User dashboard
│       ├── product_list.html               # Products page
│       ├── product_form.html               # Add/edit product form
│       ├── product_confirm_delete.html     # Delete confirmation
│       ├── record_sale.html                # Record sale form
│       ├── sales_history.html              # Sales history view
│       ├── subscription_plans.html         # Subscription tiers
│       ├── subscription_status.html        # User subscription details
│       ├── renew_subscription.html         # Subscription renewal
│       ├── admin_dashboard.html            # Admin overview
│       ├── admin_users.html                # User management
│       └── admin_subscriptions.html        # Subscription management
├── static/
│   └── images/                # Static images (carousel, etc)
├── db.sqlite3                 # Development database
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── .gitignore                 # Git ignore rules

```

## Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd smart-biz
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run migrations**
```bash
cd smartbiz
python manage.py migrate
```

6. **Create subscription plans**
```bash
python manage.py create_subscription_plans
```

7. **Create superuser (admin account)**
```bash
python manage.py createsuperuser
```

8. **Run development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Public site: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/
- User dashboard: http://localhost:8000/dashboard/

## Usage

### For End Users

1. **Register** - Create an account on the landing page
2. **Choose Plan** - Select Free, Basic, or Premium subscription
3. **Add Products** - Create your product inventory with prices
4. **Record Sales** - Log sales as they happen with quantities
5. **View Analytics** - Check dashboard for sales trends and metrics
6. **Manage Inventory** - Edit products, track low stock, delete items

### For Administrators

1. **Access Admin Dashboard** - Navigate to /admin-dashboard/
2. **Manage Users** - View all registered businesses, activate/deactivate accounts
3. **Monitor Subscriptions** - Track active subscriptions, see due renewals
4. **View Revenue** - Monitor total revenue from all subscriptions
5. **Manage Plans** - Update or modify subscription tiers as needed

## Database Models

### User Model
Extended Django User model with role-based access control (admin/staff flags)

### SubscriptionPlan
- Represents subscription tier options (Free, Basic, Premium)
- Stores pricing, duration, and feature descriptions

### Subscription
- Links users to their current subscription plan
- Tracks activation dates, expiration, and renewal status
- One-to-one relationship with User

### Product
- User inventory items with buying/selling prices
- Stock quantity tracking
- Many-to-one relationship with User

### Sale
- Transaction records for each product sale
- Quantity and total price tracking
- Timestamp for analytics
- Many-to-one relationships with User and Product

## API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /register/` - New user registration

### User Dashboard
- `GET /dashboard/` - Main dashboard with metrics
- `GET /products/` - List all products
- `POST /products/new/` - Create new product
- `POST /products/<id>/edit/` - Edit existing product
- `POST /products/<id>/delete/` - Delete product
- `GET /products/<id>/sale/` - Record sale form
- `POST /products/<id>/sale/` - Submit sale record
- `GET /sales/history/` - View all sales

### Subscriptions
- `GET /subscription/plans/` - Browse subscription tiers
- `GET /subscription/plans/<id>/renew/` - Renew/upgrade subscription
- `GET /subscription/status/` - View current subscription

### Admin
- `GET /admin-dashboard/` - Admin overview
- `GET /admin-users/` - Manage users
- `GET /admin-subscriptions/` - Manage subscriptions
- `POST /admin-users/<id>/toggle/` - Activate/deactivate user
- `POST /admin-subscriptions/<id>/toggle/` - Toggle subscription status

## Configuration

### Environment Variables (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, defaults to SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email (for password resets and notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateway (when implemented)
STRIPE_PUBLIC_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx
```

### Settings Customization
Key settings in `smartbiz/settings.py`:
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Add your domain
- `DATABASES` - Configure database connection
- `EMAIL_BACKEND` - Configure email service
- `INSTALLED_APPS` - Modify if adding new apps
- `TEMPLATES` - Template configuration

## Security Considerations

1. **Never commit .env files** - Store sensitive data in environment variables
2. **Use strong SECRET_KEY** - Change the default Django secret key
3. **Enable HTTPS** - Use SSL/TLS in production
4. **Database Security** - Use strong database passwords
5. **User Permissions** - Role-based access control is implemented
6. **CSRF Protection** - All forms include CSRF tokens
7. **SQL Injection** - Using Django ORM prevents SQL injection
8. **XSS Protection** - Django template engine escapes user input

## Performance Optimization

- Query optimization with select_related and prefetch_related
- Database indexing on frequently queried fields
- Static file caching in production
- Responsive images for mobile devices
- Minimal CSS/JS to reduce page load time
- Lazy loading for heavy components

## Testing

Run tests with:
```bash
python manage.py test
```

Test coverage includes:
- User authentication flows
- Product CRUD operations
- Sales recording and calculations
- Subscription management
- Admin dashboard functionality

## Deployment

### Development
```bash
python manage.py runserver 0.0.0.0:8000
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn smartbiz.wsgi:application --bind 0.0.0.0:8000
```

### With Docker
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "smartbiz.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Environment Setup for Production
1. Set `DEBUG=False`
2. Update `SECRET_KEY` to a strong random value
3. Configure `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL instead of SQLite
5. Set up email configuration for notifications
6. Use environment variables for all secrets
7. Enable HTTPS and security headers
8. Configure CORS if needed for API access

## Roadmap & Future Features

### Phase 2 (Q1 2025)
- Payment gateway integration (Stripe/PayPal)
- Email notifications for subscription renewals
- Advanced reporting and export to CSV/PDF
- Multi-currency support

### Phase 3 (Q2 2025)
- Multi-user support for Premium tier
- API access for Premium customers
- Mobile app (iOS/Android)
- Offline mode with sync

### Phase 4 (Q3 2025)
- Multi-location/branch management
- Custom branding for businesses
- Advanced inventory forecasting
- Integration with payment processors

## Troubleshooting

### Common Issues

**Issue: "No module named 'django'"**
- Solution: Activate virtual environment and install requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Issue: "ModuleNotFoundError: No module named 'core'"**
- Solution: Ensure you're running commands from the smartbiz directory
```bash
cd smartbiz
python manage.py runserver
```

**Issue: Database errors on first run**
- Solution: Run migrations
```bash
python manage.py migrate
python manage.py create_subscription_plans
```

**Issue: "Permission denied" for venv activation**
- Solution: Check file permissions
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@smartbiz.local
- Documentation: [Add documentation link]

## Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- Google Fonts for typography
- Built with passion for African small business owners

## Changelog

### Version 1.0.0 (December 2025)
- Initial release
- User authentication and registration
- Product inventory management
- Sales recording and tracking
- Dashboard with 7-day analytics
- Three-tier subscription system
- Admin dashboard for platform management
- Mobile-responsive design
- KES pricing for African markets

---

Made with focus on simplicity, affordability, and the needs of small business owners.
