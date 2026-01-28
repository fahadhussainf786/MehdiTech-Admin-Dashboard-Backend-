from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
import cloudinary, cloudinary.uploader
from cloudinary_utils import upload_image
from fastapi import UploadFile, File, Form, Depends
from typing import List, Optional

load_dotenv()
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


# sort the blog with filters latest and oldest
# @blog_router.get("/")
# def blog_sort(sort: str):
#  try:
#     if sort == "latest":
#         sort_blogs = supabase.table("blogs").select("*").order("created_at", desc=True).execute()

#     elif sort == "oldest":
#         sort_blogs = supabase.table("blogs").select("*").order("created_at", desc=False).execute()
#     else:
#         raise HTTPException(status_code=400, detail="Invalid sort option")

#     return sort_blogs.data
#  except Exception as e:
#         # handle unexpected db/runtime errors
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to fetch blogs: {str(e)}"
#         )


# create_blog api
@blog_router.post("")
async def create_blog(
    title: str = Form(...),  # Parameters that passes to supabase table
    content: str = Form(...),
    author: str = Form(...),
    # author_images = Form(...),
    # author_overview = Form(...),
    # cta = Form(...),
    tags: str = Form(...),
    category: str = Form(...),
    internal_images: Optional[List[UploadFile]] = File(None),
    image: Optional[UploadFile] = File(None),
    user=Depends(get_current_user),
):
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
        # Convert comma text to list
        tags_list = tags.split(",")
        try:
            supabase.table("blogs").insert(
                {
                    "title": title,
                    "content": content,
                    "thumbnail": image_url,
                    "internal_urls": internal_urls,
                    "created_by": user.user.id,
                    "author": author,
                    # "author_images": author_image,
                    # "author_overview": author_overview,
                    # "cta": cta,
                    "tags": tags_list,
                    "category": category,
                }
            ).execute()
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
@blog_router.get("")
def get_blogs():
    try:
        # Fetch all blogs from blogs table
        blogs = supabase.table("blogs").select("*").execute()
        return {"blogs": blogs.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blogs: {str(e)}")


# Update blog api
@blog_router.put("/{blog_id}")
def update_blog(blog_id: str, blog: dict, user=Depends(get_current_user)):
    try:
        # check admin or subadmin
        check_admin_or_subadmin(user)
        # update blog in blogs table
        supabase.table("blogs").update(
            {
                "title": blog["title"],
                "content": blog["content"],
                "thumbnail": blog["image_url"],
                "internal_urls": blog["internal_urls"],
                "author": blog["author"],
                "tags": blog["tags_list"],
                "category": blog["category"],
            }
        ).eq("id", blog_id).execute()

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
