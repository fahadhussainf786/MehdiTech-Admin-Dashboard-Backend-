from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from blog_apis import blog_router  # Import routers
from jobs import jobs_router
from automated_email import email_router
from applicant_job_apply import jobapply_router
from auth import get_current_user, check_admin_or_subadmin
import time
import traceback

app = FastAPI()

# Cors for giving access to frontend access
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://admin-section-mehdi-tech.vercel.app",
    "https://mehdi-technologies-admin-website.vercel.app",
    "https://admin.mehditechnologies.com",
    "https://www.mehditechnologies.com",
    "https://mehditechnologies.com",
    "https://mehditech-admin-dashboard-backend-production.up.railway.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Add middleware to handle proxy headers (HTTPS)
@app.middleware("http")
async def proxy_middleware(request: Request, call_next):
    # If the request was made via HTTPS, ensure FastAPI knows about it
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"
    return await call_next(request)


# Global exception handler to ensure CORS headers on errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error for debugging
    print(f"Global error: {exc}")
    print(f"Request origin: {request.headers.get('origin', 'No origin header')}")
    traceback.print_exc()

    # Return JSON response with CORS-friendly error
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


load_dotenv()

# Get blog routes
app.include_router(blog_router)
app.include_router(jobs_router)
app.include_router(email_router)
app.include_router(jobapply_router)
# Security
security = HTTPBearer()

# Connect with supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)


# signup and login request body to receive data
class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# api for signup
@app.post("/signup")
def signup(data: SignupRequest):
    auth_response = supabase.auth.sign_up(
        {  # Create user in supabase auth
            "email": data.email,
            "password": data.password,
        }
    )
    # Check if user creation was successful
    if auth_response.user is None:
        raise HTTPException(status_code=400, detail="Signup failed")

    # now return success message
    return {"message": "User has signed up successfully"}


# api for login
@app.post("/login")
def login(data: LoginRequest):
    auth_response = supabase.auth.sign_in_with_password(
        {  # Authenticate user
            "email": data.email,
            "password": data.password,
        }
    )
    # Check if authentication was successful
    if auth_response.session is None:
        raise HTTPException(status_code=401, detail="invalid credentials")

    # Get user role from supabase
    user = auth_response.user
    role_data = (
        supabase.table("user_roles").select("role").eq("user_id", user.id).execute()
    )
    role = role_data.data[0]["role"] if role_data.data else "user"

    # return jwt token
    return {
        "access_token": auth_response.session.access_token,
        "token_type": "bearer",
        "Role": role,
        "email": data.email,
    }


# admin api call after logged in
@app.get("/admin")  # first get get_current_user to verify token
def admin_dashboard(user=Depends(get_current_user)):
    try:
        # Fetch and check user role from user_roles table
        role_data = (
            supabase.table("user_roles")
            .select("role")
            .eq("user_id", user.user.id)
            .execute()
        )

        # if no role is found
        if role_data.data[0]["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access for Admins only")

        return {"message": "Welcome to the admin dashboard"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting admin: {str(e)}")


# #Get user profile
# @app.get("/profile")
# def get_profile(user=Depends(get_current_user)):
