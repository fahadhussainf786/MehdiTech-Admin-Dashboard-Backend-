from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
from cloudinary_utils import upload_image

load_dotenv()

jobapply_router = APIRouter(prefix="/jobapply", tags=["jobapply"])

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

# Apply for a job
@jobapply_router.post("/job_apply")
async def apply_job(
    user_email: str = Form(...),
    user_name: str = Form(...),
    resume: UploadFile = File(None)
):
    try:
        # # Check if job exists
        # job_check = supabase.table("jobs").select("id").eq("id", job_id).single().execute()
        # if not job_check.data:
        #     raise HTTPException(status_code=404, detail="Job not found")
        
        # # Check if already applied
        # existing = supabase.table("applications").select("id").eq("job_id", job_id).eq("user_email", user_email).execute()
        # if existing.data:
        #     raise HTTPException(status_code=400, detail="You have already applied for this job")
        
        # Upload resume if provided
        resume_url = None
        if resume:
            try:
                file_content = await resume.read()
                
            except Exception as resume_error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Resume upload failed: {str(resume_error)}"
                )
        # Insert application
        response = supabase.table("applications").insert({
            "user_email": user_email,
            "user_name": user_name,
            "resume_url": resume_url,
        }).execute()
        
        return {
            "message": "Application submitted successfully",
            "application_id": response.data[0]["id"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying for job: {str(e)}")

# Get all applications for a user
@jobapply_router.get("/my_applications")
def get_my_applications(user_email: str):
    """
    Get all job applications for a specific user email.
    """
    try:
        response = supabase.table("applications").select(
            "id, job_id, status, applied_at, jobs(title, department, salary_range)"
        ).eq("user_email", user_email).execute()
        
        return {"applications": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")

# # Get all applications for a job (admin only)
# @jobapply_router.get("/job/{job_id}/applications")
# def get_job_applications(job_id: str, user=Depends(get_current_user)):
#     """
#     Get all applications for a specific job (Admin/Subadmin only).
#     """
#     try:
#         check_admin_or_subadmin(user)
        
#         applications = supabase.table("applications").select(
#             "id, user_email, user_name, status, applied_at, resume_url"
#         ).eq("job_id", job_id).execute()
        
#         return {"applications": applications.data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")

# # Get single application details
# @jobapply_router.get("/applications/{app_id}")
# def get_application(app_id: str, user=Depends(get_current_user)):
#     """
#     Get details of a specific application.
#     """
#     try:
#         application = supabase.table("applications").select(
#             "id, job_id, user_email, user_name, resume_url, cover_letter, status, applied_at, jobs(title, department, salary_range)"
#         ).eq("id", app_id).single().execute()
        
#         if not application.data:
#             raise HTTPException(status_code=404, detail="Application not found")
        
#         return {"application": application.data}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching application: {str(e)}")

# Update application status (admin only)
@jobapply_router.patch("/applications/{app_id}/status")
def update_application_status(app_id: str, status: str, user=Depends(get_current_user)):
    """
    Update application status (Admin/Subadmin only).
    Status: pending, approved, rejected, under_review
    """
    try:

        response = supabase.table("applications").update({
            "status": status,
            }).eq("id", app_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"message": "Application status updated successfully"}
    
        response = supabase.table("applications").update()
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application: {str(e)}")

# Withdraw application
@jobapply_router.delete("/applications/{app_id}")
def withdraw_application(app_id: str, user=Depends(get_current_user)):
    """
    Withdraw a job application.
    """
    try:
        supabase.table("applications").delete().eq("id", app_id).execute()
        return {"message": "Application withdrawn successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error withdrawing application: {str(e)}")
