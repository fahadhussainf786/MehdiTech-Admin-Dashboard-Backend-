from fastapi import FastAPI,APIRouter, HTTPException, Depends
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin

#Job router to route job apis
jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])

load_dotenv()

app = FastAPI()
#supaabase connection
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

#Create job api
@jobs_router.post("/")
def create_job(job: dict, user=Depends(get_current_user)):

    check_admin_or_subadmin(user)

    # if not job.get("title") or not job.get("role_description"):
    #     raise HTTPException(status_code=400, detail="Missing fields")

    response = supabase.table("jobs").insert({
        "title": job["title"],  # job title
        "department": job["department"],
        "employment_type": job["emp_type"],  # job summary
        "job_description": job["job_des"],  # optional
        "qualifications": job["qualifications"],
        "salary_range": job["salary_range"],  # optional # optional
        "location": job["location"],  # optional
        "status": "draft"  # default state
    }).execute()

    return response.data

#Get one api
@jobs_router.get("/jobs/{job_id}")
def get_job(job_id: str):
    response = supabase.table("jobs").select("*").eq("id", job_id).execute()
    return response.data

#Get all jobs api
@jobs_router.get("/jobs")
def get_all_jobs():
    reponse = supabase.table("jobs").select("*").execute()
    return reponse.data

#jobs update api
@jobs_router.put("/{job_id}")
def update_job(job_id, job: dict, user=Depends(get_current_user)):
    check_admin_or_subadmin(user)

    response = supabase.table("jobs").update(job).eq("id", job_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Job not found")

    return response.data

#jobs publish api
@jobs_router.patch("/{job_id}/publish")
def publish_job(job_id, user=Depends(get_current_user)):             
    check_admin_or_subadmin(user)
    response = supabase.table("jobs").update({"status": "live"}).eq("id", job_id).execute() 
    return {"message": "Job live successfully"}

#jobs close api
@jobs_router.patch("/{job_id}/close")
def close_job(job_id, user=Depends(get_current_user)):
    check_admin_or_subadmin(user)
    response = supabase.table("jobs").update({"status": "closed"}).eq("id", job_id).execute()
    return {"message": "Job closed successfully"}

#delete job api
@jobs_router.delete("/{job_id}")
def delete_job(job_id, user=Depends(get_current_user)):

    check_admin_or_subadmin(user)

    response = supabase.table("jobs").delete().eq("id", job_id).execute()
    
    return {"message": "Job deleted successfully"}


    