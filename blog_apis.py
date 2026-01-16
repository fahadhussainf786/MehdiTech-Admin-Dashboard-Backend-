from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
from cloudinary_utils import upload_image
from fastapi import UploadFile, File, Form, Depends
from typing import List, Optional
import traceback

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

#create_blog api
@blog_router.post("/")
def create_blog(title:str = Form(...),#Parameters that passes to supabase table
                content:str = Form(...),
                author:str = Form(...),
                tags:str = Form(...),
                category: str = Form(...),
                internal_images: Optional[List[UploadFile]]= File(None),
                image: Optional[UploadFile] = File(None), user=Depends(get_current_user)):
    try:
        #Role check
        check_admin_or_subadmin(user)
        
        #upload image to cloudinary
        image_url = None
        if image:
            try:
                image_url = upload_image(image.file)
            except Exception as img_err:
                print(f"Image upload error: {img_err}")
                traceback.print_exc()
                raise HTTPException(status_code=400, detail=f"Image upload failed: {str(img_err)}")
        
        #Store internal image urls
        internal_urls = []
        if internal_images:
            for img in internal_images:
                try:
                    url = upload_image(img.file)
                    internal_urls.append(url)
                except Exception as img_err:
                    print(f"Internal image upload error: {img_err}")
                    raise HTTPException(status_code=400, detail=f"Internal image upload failed: {str(img_err)}")
        
        # Convert comma text to list
        tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        
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
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create blog error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create blog: {str(e)}")

#Get one blog api
@blog_router.get("/{blog_id}")
def get_blog(blog_id: str):
    #Fetch blog from blogs table
    blog = supabase.table("blogs").select("*").eq("id", blog_id).execute()
    
    if not blog.data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"blog": blog.data[0]}

#Get all blogs api
@blog_router.get("/")
def get_blogs():

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
        "thumbnail": blog["image_url"],
        "internal_urls": blog["internal_urls"],
        "author": blog["author"],
        "tags": blog["tags_list"],
        "category": blog["category"]
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





