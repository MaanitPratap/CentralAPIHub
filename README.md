# Central API Hub

A FastAPI-based API for accessing and processing data from multiple databases including VibrantMinds and other data sources.

## Project Structure

```
CentralAPIHub/
├── app.py                 # Main FastAPI application
├── run.py                 # Startup script
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── README.md            # This file
├── config/              # Configuration modules
│   ├── __init__.py
│   └── database.py      # Database connection management
└── databases/           # Database-specific modules
    ├── __init__.py
    ├── vibrantminds/    # VibrantMinds database
    │   ├── __init__.py
    │   ├── models.py    # VibrantMinds data models
    │   ├── service.py   # VibrantMinds business logic
    │   └── routes.py    # VibrantMinds API routes
    └── template/        # Template for new databases
        ├── __init__.py
        ├── models.py    # Template for data models
        ├── service.py   # Template for business logic
        └── routes.py    # Template for API routes
```

## Features

- **Multi-Database Support**: Each database has its own dedicated folder with models, services, and routes
- **Scalable Architecture**: Easy to add new databases by copying the template
- **Database Isolation**: Each database's logic is completely separated
- **RESTful API**: Clean, documented API endpoints
- **Error Handling**: Proper error handling and HTTP status codes
- **Data Models**: Type-safe data models using Pydantic

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Update the `.env` file with your database credentials

## Configuration

The application uses environment variables for configuration. Create a `.env` file based on `env.example`:

```env
# Future Database Configuration (for other databases)
# OTHER_DB_HOST=localhost
# OTHER_DB_PORT=5432
# OTHER_DB_DATABASE=other_db
# OTHER_DB_USER=user
# OTHER_DB_PASSWORD=password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## Running the Application

### Development
```bash
python run.py
```

### Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Root
- `GET /` - Health check and API status

### VibrantMinds Database
- `GET /vibrantminds/users` - Get all users from VibrantMinds database
- `GET /vibrantminds/sessions` - Get raw session data from VibrantMinds
- `GET /vibrantminds/sessions/readable` - Get formatted session data (without moves)
- `GET /vibrantminds/sessions/readable/extra` - Get formatted session data (with moves)
- `POST /vibrantminds/sessions/format` - Format provided session data (without moves)
- `POST /vibrantminds/sessions/format/extra` - Format provided session data (with moves)

## API Documentation

Once the application is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## Database Support

### Current Databases
- **VibrantMinds Database**: PostgreSQL database containing session data, user information, and activity details

### Adding New Databases

To add a new database:

1. **Copy the template:**
   ```bash
   cp -r databases/template databases/your_database_name
   ```

2. **Update the template files:**
   - `databases/your_database_name/models.py` - Define your data models
   - `databases/your_database_name/service.py` - Implement your business logic
   - `databases/your_database_name/routes.py` - Create your API endpoints

3. **Add database configuration:**
   - Update `config/database.py` with your database connection
   - Add environment variables to `.env`

4. **Include the router:**
   - Update `app.py` to include your new router

### Example: Adding a New Database

```python
# In app.py
from databases.your_database.routes import router as your_db_router
app.include_router(your_db_router)

# In config/database.py
@staticmethod
def get_your_database_connection():
    return psycopg2.connect(
        host=os.getenv("YOUR_DB_HOST"),
        port=int(os.getenv("YOUR_DB_PORT")),
        database=os.getenv("YOUR_DB_DATABASE"),
        user=os.getenv("YOUR_DB_USER"),
        password=os.getenv("YOUR_DB_PASSWORD")
    )
```

## Development

### Database-Specific Development
Each database folder contains:
- **models.py**: Pydantic models for data validation
- **service.py**: Business logic and data processing
- **routes.py**: API endpoints for that database

### Adding New Endpoints
1. Add your endpoint to the appropriate database's `routes.py`
2. Implement the business logic in the database's `service.py`
3. Define data models in the database's `models.py`

### Adding New Services
1. Add your service methods to the appropriate database's `service.py`
2. Import and use in your route handlers

### Adding New Models
1. Add your Pydantic models to the appropriate database's `models.py`
2. Use in your services and routes

## Error Handling

The application includes comprehensive error handling:
- Database connection errors
- Data processing errors
- Validation errors
- Proper HTTP status codes

## Contributing

1. Follow the existing project structure
2. Add proper error handling
3. Include type hints
4. Add docstrings for functions and classes
5. Test your changes
6. Use the template for new databases

## License

This project is for internal use by VibrantMinds. 