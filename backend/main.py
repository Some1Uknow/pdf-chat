from fastapi import FastAPI
from routes.upload import router as upload_router
from routes.chat import router as chat_router
from routes.files import router as files_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(upload_router, prefix="/upload")
app.include_router(chat_router, prefix="/chat")
app.include_router(files_router, prefix="/files")