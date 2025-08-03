# API Endpoints Guide

## Current Available Endpoints

### Root
- `GET /` - Health check and API status

### VibrantMinds Database
All VibrantMinds endpoints are prefixed with `/vibrantminds/`:

- `GET /vibrantminds/users` - Get all users from VibrantMinds database
- `GET /vibrantminds/sessions` - Get raw session data from VibrantMinds
- `GET /vibrantminds/sessions/readable` - Get formatted session data (without moves)
- `GET /vibrantminds/sessions/readable/extra` - Get formatted session data (with moves)
- `POST /vibrantminds/sessions/format` - Format provided session data (without moves)
- `POST /vibrantminds/sessions/format/extra` - Format provided session data (with moves)


### Testing the API

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Access the API documentation:**
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test endpoints:**
   ```bash
   # Test root endpoint
   curl http://localhost:8000/
   
   # Test VibrantMinds users
   curl http://localhost:8000/vibrantminds/users
   
   # Test VibrantMinds sessions
   curl http://localhost:8000/vibrantminds/sessions
   ```

## Troubleshooting

### Common Issues

1. **Wrong URL**: Using old URLs without the `/vibrantminds/` prefix
2. **Missing dependencies**: FastAPI not installed
3. **Database connection**: Database not running or wrong credentials
4. **Import errors**: Python path issues

### Getting Help

1. Check the server logs for error messages
2. Verify your database connection settings in `.env`
3. Test with the interactive API docs at http://localhost:8000/docs 