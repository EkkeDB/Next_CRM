# NextCRM - Commodity Trading CRM System

A comprehensive **Commodity Trading CRM System** built with Django REST Framework and Next.js, designed for commodity trading companies to manage contracts, counterparties, commodities, and analytics.

## 🚀 Features

### Backend (Django REST Framework)
- **Secure Authentication**: JWT with HttpOnly cookies, account lockout protection
- **Comprehensive Models**: 13+ business models covering commodity trading domain
- **REST API**: 50+ endpoints with filtering, search, and pagination
- **Dashboard Analytics**: Real-time statistics and charts
- **GDPR Compliance**: Data export, consent tracking, audit trails
- **Multi-currency Support**: Handle global trading operations
- **Regulatory Compliance**: Full audit logging for all operations

### Frontend (Next.js 14)
- **Modern UI**: TypeScript, Tailwind CSS, React Query
- **Interactive Dashboard**: Charts with Recharts, real-time data
- **Contract Management**: Full CRUD operations with advanced filtering
- **Responsive Design**: Mobile-friendly interface
- **Type Safety**: Comprehensive TypeScript definitions
- **State Management**: Zustand for auth, React Query for server state

### Business Domain Coverage
- **Contracts**: Lifecycle management (draft → active → completed)
- **Counterparties**: Customer/supplier relationship management
- **Commodities**: Hierarchy and trading operations
- **Traders**: Team management and responsibilities
- **Financial Tracking**: Multi-currency reporting and analytics
- **Risk Management**: Hedge tracking and exposure monitoring

## 🏗️ Architecture

```
NextCRM/
├── backend/                 # Django REST Framework
│   ├── core/               # Main Django project
│   ├── apps/
│   │   ├── authentication/ # JWT auth, GDPR compliance
│   │   └── nextcrm/        # Business logic models
│   └── requirements.txt
├── frontend/               # Next.js 14 with TypeScript
│   ├── src/
│   │   ├── app/           # Next.js App Router
│   │   ├── components/    # Reusable UI components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── lib/           # Utilities and API client
│   │   └── types/         # TypeScript definitions
│   └── package.json
└── docker-compose.yml     # Container orchestration
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL (for local development)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Next_CRM
   ```

2. **Start with Docker Compose**
   ```bash
   # Development environment
   docker-compose -f docker-compose.dev.yml up --build

   # Production environment
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

### Option 2: Local Development

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL

# Start development server
npm run dev
```

## 📊 Core Models

### Business Entities
- **Contract**: Main trading contract with full lifecycle
- **Counterparty**: Trading partners (customers/suppliers)
- **Commodity**: Product hierarchy and specifications
- **Trader**: Team members and responsibilities
- **Currency**: Multi-currency support with exchange rates

### Reference Data
- **Cost Centers**: Organizational cost tracking
- **Sociedades**: Legal entities/companies
- **Commodity Groups/Types**: Product categorization

### Compliance & Security
- **User Profiles**: Extended user information with GDPR consent
- **Audit Logs**: Complete action tracking for compliance
- **GDPR Records**: Consent management and data rights
- **Login Attempts**: Security monitoring and account protection

## 🔒 Security Features

- **JWT Authentication**: HttpOnly cookies for secure token storage
- **Account Protection**: Failed login attempt tracking and lockout
- **GDPR Compliance**: Data export, consent tracking, right to deletion
- **Audit Trails**: Complete action logging for regulatory compliance
- **CORS Configuration**: Secure cross-origin resource sharing
- **Input Validation**: Comprehensive data validation and sanitization

## 📈 Dashboard Analytics

- **Contract Statistics**: Total, active, completed, overdue counts
- **Financial Metrics**: Portfolio value, revenue trends
- **Visual Charts**: Monthly trends, status distribution, top commodities
- **Delivery Tracking**: Upcoming deliveries and deadlines
- **Performance Insights**: Top counterparties and commodities by value

## 🛠️ Development

### Backend Commands
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Load sample data
python manage.py loaddata fixtures/sample_data.json
```

### Frontend Commands
```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

## 🚀 Deployment

### Production Deployment
1. **Configure environment variables**
   ```bash
   # Backend
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   DB_PASSWORD=secure-database-password
   
   # Frontend
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Set up reverse proxy** (Nginx configuration included)

### Environment Variables

#### Backend (.env)
```env
SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=nextcrm
DB_USER=nextcrm_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=NextCRM
```

## 📚 API Documentation

The API provides comprehensive endpoints for all business operations:

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration
- `GET /api/auth/profile/` - User profile
- `POST /api/auth/token/refresh/` - Token refresh

### Core Business
- `GET /api/nextcrm/contracts/` - List contracts
- `POST /api/nextcrm/contracts/` - Create contract
- `GET /api/nextcrm/contracts/{id}/` - Contract details
- `PUT /api/nextcrm/contracts/{id}/` - Update contract
- `POST /api/nextcrm/contracts/{id}/approve/` - Approve contract

### Reference Data
- `GET /api/nextcrm/counterparties/` - List counterparties
- `GET /api/nextcrm/commodities/` - List commodities
- `GET /api/nextcrm/traders/` - List traders
- `GET /api/nextcrm/currencies/` - List currencies

### Analytics
- `GET /api/nextcrm/contracts/dashboard_stats/` - Dashboard statistics
- `GET /api/nextcrm/search/?q=term` - Global search

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` folder
- Review the API documentation at `/api/docs/` when running

## 🎯 Roadmap

- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] AI-powered insights
- [ ] Advanced risk management
- [ ] Integration with external trading platforms
- [ ] Multi-language support
- [ ] Advanced workflow automation

---

**NextCRM** - Professional commodity trading management for the modern world.