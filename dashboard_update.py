# from fastapi import FastAPI, APIRouter, HTTPException
# import os
# from dotenv import load_dotenv
# from supabase import create_client

# #Api router for routes
# dashboard_router = APIRouter(prefix="/dashboard", tags="dashboard")

# #SUPABASE CONFIG
# supabase = create_client(
#     os.getenv("SUPABASE_URL"),
#     os.getenv("SUPABASE_SERVICE_ROLE_KEY")
# )
# #get api for blogs data
# @dashboard_router.get("/")
# def get_dashboard_update():
#     response = supabase.table("blogs").select("*")({

#     })
