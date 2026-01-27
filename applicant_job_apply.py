from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from supabase import create_client
import os
import uuid
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
@jobapply_router.post("/job_apply/{job_id}")
async def apply_job(
    job_id: str,
    user_email: str = Form(...),
    name: str = Form(...),
    phone_number: str = Form(None),
    resume: UploadFile = File(None), user=Depends(get_current_user)
):
    try:
       
        # Check if job exists
        job_check = supabase.table("jobs").select("id").eq("id", job_id).single().execute()
        if not job_check.data:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check if already applied
        existing = supabase.table("applications").select("id").eq("job_id", job_id).eq("user_email", user_email).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="You have already applied for this job")
        
        #resume optional
        resume_url = None #default none
        if resume:
          file_name = f"{uuid.uuid4()}.pdf"

        # we have to store resume in supabase storage
          supabase.storage.from_("resumes").upload(
            file_name,
            await resume.read(),
            {"content-type": resume.content_type}
        )
        #Now get the resume url
          resume_url = supabase.storage.from_("resumes").get_public_url(file_name)

        # Insert application
        response = supabase.table("applications").insert({
            "job_id": job_id,
            "user_id": user.user.id,
            "user_email": user_email,
            "applicant_name": name,
            "resume_url": resume_url,
            "phone_number": phone_number,
            "status": "Applied"
        }).execute()
        
        return {
            "message": "Application submitted successfully",
            "application_id": response.data[0]["id"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error applying for job: {str(e)}")

#get applicants data from applications
@jobapply_router.get("/{job_id}/applicants/count")
def get_applicants(job_id: str):
    #check for unique userid
    response = supabase.table("applications")\
    .select("user_id",count="exact")\
    .eq("job_id", job_id).execute()
    return {"total applicants": response.count}

# Get all applications for a user
@jobapply_router.get("/my_applications")
def get_my_applications():
    try:
        #Get applications
        response = supabase.table("applications").select(
            "id,applicant_name,user_email, status"
        ).execute()
        
        return {"applications": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching applications: {str(e)}")
# Get single application details
@jobapply_router.get("/applications/{app_id}")
def get_application(app_id: str):
    
    try:
        application = supabase.table("applications").select(
            "id, job_id, user_email, user_name, resume_url, cover_letter, status, applied_at, jobs(title, department, salary_range)"
        ).eq("id", app_id).single().execute()
        
        if not application.data:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"application": application.data}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching application: {str(e)}")

# Update application status
@jobapply_router.patch("/applications/{app_id}/status")
def update_application_status(app_id: str, status: str):
    try:
        response = supabase.table("applications").update({
            "status": status,
            }).eq("id", app_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return {"message": "Application status updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application: {str(e)}")

# Withdraw application
@jobapply_router.delete("/applications/{app_id}")
def withdraw_application(app_id: str, user=Depends(get_current_user)):
    try:
        supabase.table("applications").delete().eq("id", app_id).execute()
        return {"message": "Application withdrawn successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error withdrawing application: {str(e)}")
