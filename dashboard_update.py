from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
import os
from supabase import create_client

#api router for routes
dashboard_router = APIRouter(prefix= "/dashboard", tags=["dashboard"])

#supabase configure
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

#get api for getting blogs data
@dashboard_router.get("/get_blogs")
def dashboard_get_blogs():

    response = supabase.table("blogs")\
        .select("id", count="exact")\
        .execute()
    
    return("Found blogs", response.count)

#get api for getting jobs
@dashboard_router.get("/get_jobs")
def dashboard_get_jobs():
    response = supabase.table("jobs")\
         .select("id", count="exact")\
         .eq("status", "live")\
         .execute()
    
    return("Found live jobs ", response.count)

#Get pending applicants from applications
@dashboard_router.get("/get_applicants")
def dashboard_get_applicants():
    response = supabase.table("applications")\
          .select("id", count= "exact")\
          .eq("status", "Applied")\
          .execute()
    return ("Found applicants", response.count)
