from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import search, contact
from app.core.config import settings

app = FastAPI(
    title="Personal Website API",
    description="Backend API for personal website with AI search functionality",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(contact.router, prefix="/api", tags=["contact"])

@app.get("/")
async def root():
    return {"message": "Personal Website API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
