from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
import cloudinary
import cloudinary.uploader
from cloudinary_utils import upload_image
from fastapi import UploadFile, File, Form, Body, Depends
from typing import List, Optional

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("Cloudinary_CLOUD_NAME"),
    api_key=os.getenv("Cloudinary_API_KEY"),
    api_secret=os.getenv("Cloudinary_API_SECRET")
)

# Create router for blogs
blog_router = APIRouter(prefix="/blogs", tags=["blogs"])

# supabase connection
supabase = create_client(
    os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
# Setup bearer authentication
security = HTTPBearer()

# Make api for uploading image
@blog_router.post("/uploadimage")
async def upload_image_endpoint(image_file: UploadFile = File(None)):
    if not image_file:
        raise HTTPException(status_code=400, detail="No file provided")
    file_content = await image_file.read()
    response = cloudinary.uploader.upload(file_content)
    return {"url": response.get("secure_url")}

#create_blog api
@blog_router.post("/")
async def create_blog(title:str = Form(...),#Parameters that passes below supabase table
                content:str = Form(...),
                author:str = Form(...),
                author_image: Optional[UploadFile] = File(None),
                author_overview:str = Form(...),
                meta_title: Optional[str]= Form(...),
                meta_description:Optional[str] = Form(...),
                keywords: Optional[str] = Form(None),
                thumbnail_image: Optional[UploadFile] = File(None),
                cta:str = Form(...),
                slug: Optional[str]= Form(...),
                tags:str = Form(...),
                category: str = Form(...),
                internal_images: Optional[List[UploadFile]]= File(None),
                image: Optional[UploadFile] = File(None), user=Depends(get_current_user)):
    try:
        check_admin_or_subadmin(user)
        image_url = None  # default none
        if image:
            try:
                file_content = await image.read()
                image_url = upload_image(file_content)
            except Exception as img_error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Thumbnail image not found: {str(img_error)}",
                )
        # Store internal image urls
        internal_urls = []
        if internal_images:
            for img in internal_images:
                try:
                    file_content = await img.read()
                    url = upload_image(file_content)
                    internal_urls.append(url)
                except Exception as img_error:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Internal image upload failed: {str(img_error)}",
                    )
    
        #get authorimage url
        author_image_url = None
        if author_image:
            try:
                file_content = await author_image.read()
                author_image_url = upload_image(file_content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Author image upload failed: {str(e)}"
                )
            
        #Get thumbnail image url
        thumbnail_image_url = None
        if thumbnail_image:
            try:
                file_content = await thumbnail_image.read()
                thumbnail_image_url = upload_image(file_content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Thumbnail image upload failed: {str(e)}"
                )
        
        # Convert comma text to list
        tags_list = tags.split(",")
        keywords_list = [k.strip() for k in keywords.split(",")]

        try:
            supabase.table("blogs").insert({
                "title": title,
                "content": content,
                "thumbnail": image_url,
                "internal_urls": internal_urls,
                "meta_title": meta_title,
                "meta_description": meta_description,
                "keywords": keywords_list,
                "slug": slug,
                "created_by": user.user.id,
                "author": author,
                "author_images": author_image_url,
                "author_overview": author_overview,
                "thumbnail_image": thumbnail_image_url,
                "cta": cta,
                "tags": tags_list,
                "category": category
            }).execute()
        except Exception as db_error:
            raise HTTPException(
                status_code=400, detail=f"Failed to save blog: {str(db_error)}"
            )
        # Return success message
        return {"message": "Blog created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Get one blog api
@blog_router.get("/{blog_id}")
def get_blog(blog_id: str):
    try:
        # Fetch blog from blogs table
        blog = supabase.table("blogs").select("*").eq("id", blog_id).execute()

        if not blog.data:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"blog": blog.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blog: {str(e)}")

# Get all blogs api
@blog_router.get("/")
def get_blogs():
    try:
        # Fetch all blogs from blogs table
        blogs = supabase.table("blogs").select("*").execute()
        return {"blogs": blogs.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blogs: {str(e)}")

# Update blog api
@blog_router.patch("/{blog_id}")
async def update_blog(blog_id: str,
                title: Optional[str] = Form(None),
                content: Optional[str] = Form(None),
                author: Optional[str] = Form(None),
                author_overview: Optional[str] = Form(None),
                meta_title: Optional[str] = Form(None),
                meta_description: Optional[str] = Form(None),
                keywords: Optional[str] = Form(None),
                cta: Optional[str] = Form(None),
                slug: Optional[str] = Form(None),
                tags: Optional[str] = Form(None),
                category: Optional[str] = Form(None),
                image: Optional[UploadFile] = File(None),
                thumbnail_image: Optional[UploadFile] = File(None),
                author_image: Optional[UploadFile] = File(None),
                internal_images: Optional[List[UploadFile]]= File(None),
                user=Depends(get_current_user)):
    try:
        # check admin or subadmin
        check_admin_or_subadmin(user)
        image_url = None  # default none
        if image:
            try:
                file_content = await image.read()
                image_url = upload_image(file_content)
            except Exception as img_error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Thumbnail image not found: {str(img_error)}",
                )
        # Store internal image urls
        internal_urls = []
        if internal_images:
            for img in internal_images:
                try:
                    file_content = await img.read()
                    url = upload_image(file_content)
                    internal_urls.append(url)
                except Exception as img_error:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Internal image upload failed: {str(img_error)}",
                    )
    
        #get authorimage url
        author_image_url = None
        if author_image:
            try:
                file_content = await author_image.read()
                author_image_url = upload_image(file_content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Author image upload failed: {str(e)}"
                )
            
        #Get thumbnail image url
        thumbnail_image_url = None
        if thumbnail_image:
            try:
                file_content = await thumbnail_image.read()
                thumbnail_image_url = upload_image(file_content)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Thumbnail image upload failed: {str(e)}"
                )

        # Prepare update data - only include fields that are provided
        update_data = {}
        
        if title is not None:
            update_data["title"] = title
        if content is not None:
            update_data["content"] = content
        if image_url is not None:
            update_data["thumbnail"] = image_url
        if internal_urls:
            update_data["internal_urls"] = internal_urls
        if author_image_url is not None:
            update_data["author_images"] = author_image_url
        if author_overview is not None:
            update_data["author_overview"] = author_overview
        if meta_title is not None:
            update_data["meta_title"] = meta_title
        if meta_description is not None:
            update_data["meta_description"] = meta_description
        if keywords is not None:
            update_data["keywords"] = [k.strip() for k in keywords.split(",")]
        if slug is not None:
            update_data["slug"] = slug
        if thumbnail_image_url is not None:
            update_data["thumbnail_image"] = thumbnail_image_url
        if cta is not None:
            update_data["cta"] = cta
        if author is not None:
            update_data["author"] = author
        if tags is not None:
            update_data["tags"] = tags.split(",")
        if category is not None:
            update_data["category"] = category

        #update blog in blogs table
        if update_data:
            supabase.table("blogs").update(update_data).eq("id", blog_id).execute()

        return {"message": "Blog updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating blog: {str(e)}")


# Delete blog api
@blog_router.delete("/{blog_id}")
def delete_blog(blog_id: str, user=Depends(get_current_user)):
    try:
        # check admin or subadmin
        check_admin_or_subadmin(user)
        # delete blog from blogs table
        supabase.table("blogs").delete().eq("id", blog_id).execute()
        return {"message": "Blog deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting blog: {str(e)}")