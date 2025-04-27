from fastapi import FastAPI, Request
from routes.upload import router as upload_router
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

load_dotenv()

# Initialize limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

# Add rate limiting middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Get allowed origins from environment variable or use default
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload")
app.include_router(chat_router, prefix="/chat")

@app.get("/health")
@limiter.limit("10/minute")
async def health_check(request: Request):
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}