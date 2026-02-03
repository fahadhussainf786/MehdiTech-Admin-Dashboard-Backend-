from fastapi import APIRouter, HTTPException, Depends
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
from typing import Dict, Any, List

load_dotenv()

# Create router for dashboard
dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Supabase connection
supabase = create_client(
    os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

@dashboard_router.get("/stats")
async def get_dashboard_stats(user=Depends(get_current_user)):
    """
    Get dashboard statistics including total blogs, jobs, and other metrics
    """
    try:
        check_admin_or_subadmin(user)
        
        # Get total blogs count
        blogs_response = supabase.table("blogs").select("id", count="exact").execute()
        total_blogs = blogs_response.count or 0
        
        # Get total jobs count
        jobs_response = supabase.table("jobs").select("id", count="exact").execute()
        total_jobs = jobs_response.count or 0
        
        # Get live jobs count
        live_jobs_response = supabase.table("jobs").select("id", count="exact").eq("status", "live").execute()
        live_jobs = live_jobs_response.count or 0
        
        # Get closed jobs count
        closed_jobs_response = supabase.table("jobs").select("id", count="exact").eq("status", "closed").execute()
        closed_jobs = closed_jobs_response.count or 0
        
        return {
            "total_blogs": total_blogs,
            "total_jobs": total_jobs,
            "live_jobs": live_jobs,
            "closed_jobs": closed_jobs
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard stats: {str(e)}")

@dashboard_router.get("/blogs")
async def get_dashboard_blogs(
    limit: int = 10,
    offset: int = 0,
    user=Depends(get_current_user)
):
    """
    Get recent blogs for dashboard
    """
    try:
        check_admin_or_subadmin(user)
        
        # Get recent blogs with pagination
        response = supabase.table("blogs")\
            .select("id, title, author, created_at, category, status")\
            .order("created_at", desc=True)\
            .range(offset, offset + limit - 1)\
            .execute()
        
        return {
            "blogs": response.data,
            "total_count": len(response.data)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard blogs: {str(e)}")

@dashboard_router.get("/jobs")
async def get_dashboard_jobs(
    limit: int = 10,
    offset: int = 0,
    status: str = None,
    user=Depends(get_current_user)
):
    """
    Get recent jobs for dashboard with optional status filter
    """
    try:
        check_admin_or_subadmin(user)
        
        query = supabase.table("jobs")\
            .select("id, title, department, employment_type, location, status, created_at")\
            .order("created_at", desc=True)
        
        # Apply status filter if provided
        if status:
            query = query.eq("status", status)
        
        response = query.range(offset, offset + limit - 1).execute()
        
        return {
            "jobs": response.data,
            "total_count": len(response.data)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard jobs: {str(e)}")

@dashboard_router.get("/recent-activity")
async def get_recent_activity(user=Depends(get_current_user)):
    """
    Get recent activity across blogs and jobs
    """
    try:
        check_admin_or_subadmin(user)
        
        # Get recent blogs
        blogs_response = supabase.table("blogs")\
            .select("id, title, created_at, author")\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()
        
        # Get recent jobs
        jobs_response = supabase.table("jobs")\
            .select("id, title, created_at, status")\
            .order("created_at", desc=True)\
            .limit(5)\
            .execute()
        
        # Combine and format activities
        activities = []
        
        # Add blog activities
        for blog in blogs_response.data:
            activities.append({
                "id": blog["id"],
                "title": blog["title"],
                "type": "blog",
                "author": blog.get("author", "Unknown"),
                "created_at": blog["created_at"],
                "status": "published"
            })
        
        # Add job activities
        for job in jobs_response.data:
            activities.append({
                "id": job["id"],
                "title": job["title"],
                "type": "job",
                "department": job.get("department", "Unknown"),
                "created_at": job["created_at"],
                "status": job.get("status", "live")
            })
        
        # Sort by created_at
        activities.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "activities": activities[:10]  # Return latest 10 activities
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recent activity: {str(e)}")

@dashboard_router.get("/analytics")
async def get_dashboard_analytics(user=Depends(get_current_user)):
    """
    Get detailed analytics for dashboard
    """
    try:
        check_admin_or_subadmin(user)
        
        # Get blogs by category
        blogs_by_category = supabase.table("blogs")\
            .select("category")\
            .execute()
        
        category_counts = {}
        for blog in blogs_by_category.data:
            category = blog.get("category", "uncategorized")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Get jobs by department
        jobs_by_department = supabase.table("jobs")\
            .select("department")\
            .execute()
        
        department_counts = {}
        for job in jobs_by_department.data:
            department = job.get("department", "unknown")
            department_counts[department] = department_counts.get(department, 0) + 1
        
        # Get jobs by employment type
        jobs_by_type = supabase.table("jobs")\
            .select("employment_type")\
            .execute()
        
        type_counts = {}
        for job in jobs_by_type.data:
            emp_type = job.get("employment_type", "unknown")
            type_counts[emp_type] = type_counts.get(emp_type, 0) + 1
        
        return {
            "blogs_by_category": category_counts,
            "jobs_by_department": department_counts,
            "jobs_by_employment_type": type_counts
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")