import cloudinary
from cloudinary import uploader
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from fastapi import status
from config import CLOUDINARY_CLOUD_API_KEY, CLOUDINARY_CLOUD_NAME, CLOUDINARY_CLOUD_API_SECRET

cloudinary.config(cloud_name=CLOUDINARY_CLOUD_NAME,
                  api_key=CLOUDINARY_CLOUD_API_KEY, api_secret=CLOUDINARY_CLOUD_API_SECRET)

def upload_pic(pic: UploadFile) -> str:
    if pic.filename.endswith(".jpg") or pic.filename.endswith(".png"):
            result = uploader.upload(pic.file)
            url = result.get("url")
            return url
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Not a picture")
