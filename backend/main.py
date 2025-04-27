from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/upload")
app.include_router(chat_router, prefix="/chat")