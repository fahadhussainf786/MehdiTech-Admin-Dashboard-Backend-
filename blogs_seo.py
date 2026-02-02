from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import get_current_user, check_admin_or_subadmin
from fastapi import UploadFile, File, Body, Form
import cloudinary, cloudinary.uploader 
from cloudinary_utils import upload_image 
from typing import List, Optional
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

#supabase configure
supabase= create_client(
    os.getenv('SUPABASE_URL'), 
    os.getenv('SUPABASE_SERVICE_ROLE_KEY')
)
#create raouter for blogs_seo
blog_seo_router = APIRouter(prefix="/blogs_seo", tags=["blogs_seo"])

#create blogs_seo api key 
@blog_seo_router.post("/{blog_id}")
async def create_blogs_seo(blog_id: str, 
                     meta_title: str =Form(...),
                     meta_description: str= Form(...),
                     keywords: str = Form(...),
                     slug: str = Form(...), 
                     image: Optional[UploadFile] = File(None), 
                     user= Depends(get_current_user)):
    try:
        check_admin_or_subadmin(user)

        image_url = None
        if image:
                file_content = await image.read()
                image_url = upload_image(file_content)
        # keywords list
        keywords_list = [k.strip() for k in keywords.split(",")]

        supabase.table("blogs_seo").insert({
            "blog_id": blog_id,                       # REQUIRED
            "meta_title": meta_title,
            "meta_description":meta_description,
            "keywords": keywords_list,               # USING keywords
            "thumbnail": image_url,                   # USING thumbnail
            "slug": slug
        }).execute()

        return{"blogs seo successfull"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#now update the blogs_seo
@blog_seo_router.patch("/{blog_id}")
async def update_blog_seo(blog_id: str,
                    meta_title: str = Form(...),
                    meta_description: str = Form(...),
                    keywords: str = Form(...),
                    slug: str = Form(...), 
                    image:Optional[UploadFile] =File(None),
                    user=Depends(get_current_user)):
    try:
        check_admin_or_subadmin(user)
        image_url = None
        if image:
            file_content = await image.read()
            image_url = upload_image(file_content)

        keywords_list = [k.strip() for k in keywords.split(",")]

        supabase.table("blogs_seo").update({
            "meta_title": meta_title,
            "meta_description": meta_description,
            "keywords": keywords_list,
            "thumbnail": image_url,
            "slug": slug
        }).eq("blog_id", blog_id).execute()

        return {"message": "blog seo updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blog: {str(e)}")


#Now get all blogs_seo
@blog_seo_router.get("/{blog_id}")
def get_all_blogs_seo(blog_id: str):
     
 try:
     supabase.table("blogs_seo").select("*").eq("blog_id", blog_id).execute()
     
     return {"Get blogs "}
 except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blog: {str(e)}")