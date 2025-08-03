from fastapi import FastAPI
from databases.vibrantminds.routes import router as vibrantminds_router

app = FastAPI(
    title="Central API Hub",
    description="API for VibrantMinds Database and other data sources",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Central API Hub is running!"}

# Include database-specific routers
app.include_router(vibrantminds_router)

# Future: Add other database routers here
# Example: app.include_router(otherdb_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 