# AgriSense Backend

Smart agriculture monitoring system with weather early warning and pest risk management.

## Features

### Core Features
1. **Weather Early Warning System** 🌤️
   - Real-time weather monitoring
   - 5-day weather forecast
   - Automatic weather alerts
   - Agricultural recommendations

2. **Pest Risk Management** 🐛
   - Image-based pest detection
   - AI-powered identification (mock ML)
   - Severity assessment
   - Treatment recommendations

### Supporting Features
- **Sensor Data Management** - Temperature, humidity, soil moisture, rainfall tracking
- **Alert System** - Automated alerts for weather, pests, and sensor anomalies
- **User Authentication** - JWT-based authentication with 30-day tokens

## Tech Stack

- **Framework:** FastAPI 0.104.1
- **Database:** SQLAlchemy 2.0.23 + Alembic (migrations)
- **Authentication:** JWT (python-jose) + bcrypt
- **Image Processing:** Pillow 10.1.0
- **Weather API:** OpenWeatherMap
- **Testing:** pytest + pytest-asyncio

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── dependencies/         # FastAPI dependencies (auth)
├── models/              # SQLAlchemy models
├── routers/             # API endpoints
├── schemas/             # Pydantic schemas
├── services/            # Business logic (weather, alerts)
├── tests/               # Test suite
├── utils/               # Utilities (password, JWT, file storage)
├── database.py          # Database configuration
├── main.py              # FastAPI application
├── config.py            # Settings configuration
└── run.py               # Development server

uploads/                 # Uploaded pest images
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./agrisense.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production

# Weather API
OPENWEATHER_API_KEY=your-openweathermap-api-key

# Environment
ENVIRONMENT=development
```

Get OpenWeatherMap API key: https://openweathermap.org/api

### 3. Initialize Database

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Seed Test Data (Optional)

```bash
python seed_data.py
```

Creates:
- Test user (username: `testuser`, password: `password123`)
- Sample sensor data
- Sample pest detections
- Sample alerts

### 5. Run Development Server

```bash
python run.py
```

Server runs at: http://localhost:5000

## API Documentation

### Interactive Docs
- **Swagger UI:** http://localhost:5000/swagger
- **ReDoc:** http://localhost:5000/redoc

### Full Documentation
See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API reference.

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=html
```

View coverage report: `htmlcov/index.html`

### Run Specific Tests

```bash
# Authentication tests only
pytest tests/test_auth.py

# Sensor tests only
pytest tests/test_sensor.py

# Alert tests only
pytest tests/test_alert.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_auth.py::TestUserRegistration::test_register_new_user
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only auth tests
pytest -m auth
```

## Database Migrations

### Create Migration

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description"
```

### Apply Migrations

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade one version
alembic upgrade +1

# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>
```

### View Migration History

```bash
# Show current version
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --verbose
```

## Development

### Code Quality

```bash
# Format code
black backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/
```

### Adding New Endpoints

1. Create model in `models/`
2. Create schema in `schemas/`
3. Create router in `routers/`
4. Register router in `main.py`
5. Create migration: `alembic revision --autogenerate -m "Add model"`
6. Apply migration: `alembic upgrade head`
7. Write tests in `tests/`

### Adding New Dependencies

```bash
# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt
```

## Production Deployment

### Database

Migrate from SQLite to PostgreSQL:

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary asyncpg
```

2. Update `DATABASE_URL` in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/agrisense
```

3. Run migrations:
```bash
alembic upgrade head
```

### Security

1. **Change SECRET_KEY** - Use strong random key
2. **Enable HTTPS** - Use SSL/TLS certificates
3. **Set CORS origins** - Restrict to your frontend domain
4. **Add rate limiting** - Prevent abuse
5. **Enable logging** - Monitor for security issues

### Performance

1. **Use PostgreSQL** - Better performance than SQLite
2. **Add caching** - Redis for weather data, alerts
3. **Optimize queries** - Add indexes, use eager loading
4. **Use CDN** - For uploaded images
5. **Enable compression** - Gzip responses

### Monitoring

1. **Add logging** - Use structured logging (loguru)
2. **Add metrics** - Prometheus + Grafana
3. **Add error tracking** - Sentry
4. **Add health checks** - `/health` endpoint
5. **Add uptime monitoring** - UptimeRobot, Pingdom

## Troubleshooting

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm agrisense.db
alembic upgrade head
python seed_data.py
```

### Migration Issues

```bash
# Reset migrations (WARNING: deletes migration history)
rm -rf alembic/versions/*.py
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Import Errors

```bash
# Ensure backend is in Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

### Port Already in Use

```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

## Contributing

1. Create feature branch
2. Make changes
3. Write tests
4. Run tests: `pytest`
5. Format code: `black backend/`
6. Create pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Create issue]
- Documentation: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Alembic Guide: [../.references/ALEMBIC_SETUP_GUIDE.md](../.references/ALEMBIC_SETUP_GUIDE.md)
