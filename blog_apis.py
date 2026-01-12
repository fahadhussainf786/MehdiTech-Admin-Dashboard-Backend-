from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user
from cloudinary_utils import upload_image
from fastapi import UploadFile, File, Form, Depends
from typing import List, Optional

load_dotenv()
#Create router for blogs
blog_router = APIRouter(prefix="/blogs", tags=["blogs"])

#supabase connection
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
#Setup bearer authentication
security = HTTPBearer()

#Make Function for Role check
def check_admin_or_subadmin(user):
    #Fetch user role from user_roles table
    role_data = supabase.table("user_roles").select("role").eq("user_id", user.user.id).execute()
    #if no role is found 
    if not role_data.data:
        raise HTTPException(status_code=403, detail="Role not found")
    # Get the role
    role = role_data.data[0]['role']
    #Role check for admin and subadmin
    if role_data.data[0]['role'] not in ['admin', 'subadmin']:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins and Subadmins only")

    return role
#create_blog api
@blog_router.post("/")
def create_blog(title:str = Form(...),#Parameters that passes to supabase table
                content:str = Form(...),
                author:str = Form(...),
                tags:str = Form(...),
                category: str = Form(...),
                internal_images: Optional[list[UploadFile]]= File(None),
                image:UploadFile = File(...), user=Depends(get_current_user)):

    #Role check
    check_admin_or_subadmin(user)
    #upload image to cloudinary
    image_url = upload_image(image.file)
    #Store internal image urls
    internal_urls = []
    if internal_images:
        for img in internal_images:
            url = upload_image(img.file)
            internal_urls.append(url)

    # Convert comma text to list
    tags_list = tags.split(",")
    #Insert blog into blogs table
    supabase.table("blogs").insert({
        "title": title,
        "content": content,
        "thumbnail": image_url,
        "internal_urls": internal_urls,
        "created_by": user.user.id,
        "author": author,
        "tags": tags_list,
        "category": category
    }).execute()
    #Return success message
    return {"message": "Blog created successfully"}

#Get all blogs api
@blog_router.get("/")
def get_blogs(user=Depends(get_current_user)):

    check_admin_or_subadmin(user)
    #Fetch all blogs from blogs table
    blogs = supabase.table("blogs").select("*").execute()

    return {"blogs": blogs.data}

#Update blog api
@blog_router.put("/{blog_id}")
def update_blog(blog_id: str, blog: dict, user=Depends(get_current_user)):
    #check admin or subadmin
    check_admin_or_subadmin(user)
    #update blog in blogs table
    supabase.table("blogs").update({
        "title": blog["title"],
        "content": blog["content"],
        "images_url": blog["images_url"]
    }).eq("id", blog_id).execute()

    return {"message": "Blog updated successfully"}

#Delete blog api
@blog_router.delete("/{blog_id}")
def delete_blog(blog_id: str, user=Depends(get_current_user)):
    #check admin or subadmin
    check_admin_or_subadmin(user)
    #delete blog from blogs table
    supabase.table("blogs").delete().eq("id", blog_id).execute()

    return {"message": "Blog deleted successfully"}





