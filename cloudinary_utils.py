import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()
#Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("Cloudinary_CLOUD_NAME"),
    api_key=os.getenv("Cloudinary_API_KEY"),
    api_secret=os.getenv("Cloudinary_API_SECRET")
)
#First upload image to cloudinary and get the url
def upload_image(image_file):
    response = cloudinary.uploader.upload(image_file)
    return response.get("secure_url")



