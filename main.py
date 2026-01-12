from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv
from blog_apis import blog_router
from auth import get_current_user

load_dotenv()

app = FastAPI()
#Get blog routes
app.include_router(blog_router)
#Security 
security = HTTPBearer()

#Connect with supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
#signup and login request body to receive data
class SignupRequest(BaseModel):
    email: str
    password: str
    
class LoginRequest(BaseModel):
    email: str
    password: str

#api for signup
@app.post("/signup")
def signup(data: SignupRequest):
    auth_response = supabase.auth.sign_up({#Create user in supabase auth
        "email": data.email,
        "password": data.password

})
    #Check if user creation was successful
    if auth_response.user is None:
        raise HTTPException(status_code=400, detail="Signup failed")
    
    #now return success message
    return {"message": "User has signed up successfully"}

#api for login
@app.post("/login")
def login(data: LoginRequest):
    auth_response = supabase.auth.sign_in_with_password({#Authenticate user
        "email": data.email,
        "password": data.password
})
    #Check if authentication was successful
    if auth_response.session is None:
        raise HTTPException(status_code=401, detail="invalid credentials")

    #return jwt token
    return {
        "access_token": auth_response.session.access_token,
        "token_type": "bearer"
    }

#admin api call after logged in
@app.get("/admin") #first run get_current_user to verify token
def admin_dashboard(user=Depends(get_current_user)):
    #Match the currently loggedin user with user in table
    role_data = supabase.table("user_roles").select("role").eq("user_id", user.user.id).execute()
     #Check if user is not admin
     #if no role is found
    if not role_data.data:
        raise HTTPException(status_code=403, detail="Role not found")
    if role_data.data[0]['role'] != 'admin':
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    
    return {"message": "Welcome to the admin dashboard"}

# @app.get("/")
# def root():
#     return {"status": "working"}



