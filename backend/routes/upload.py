from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
from dotenv import load_dotenv
from utils.storemeta import store_meta
from utils.storedata import store_data
import magic

# Load environment variables
load_dotenv()

router = APIRouter()

# Directory for uploads
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("")
async def upload(file: UploadFile = File(...), user_gmail: str = ""):
    # Check file size
    file.file.seek(0, 2)  # Seek to end of file
    file_size = file.file.tell()  # Get current position (file size)
    file.file.seek(0)  # Reset file position
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    
    # Verify file type
    file_content = await file.read(2048)  # Read first 2048 bytes for MIME detection
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_content)
    
    if file_type != 'application/pdf':
        raise HTTPException(status_code=415, detail="Only PDF files are allowed.")
    
    # Reset file position after reading
    await file.seek(0)
    
    try:
        # Define the path to save the uploaded file
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        
        # Write the file to the uploads directory
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Store metadata in the database and retrieve the file_id
        file_id = store_meta(file_location, file.filename, file_size, file_type, user_gmail)
        
        if not file_id:
            raise HTTPException(status_code=500, detail="Failed to store file metadata")
        
        # Process and store file data
        await store_data(file_location, file_id)
        
        return {
            "message": "File uploaded and processed successfully",
            "file_location": file_location,
            "file_id": file_id
        }
        
    except Exception as e:
        # Clean up the file if it was uploaded
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))
