from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client
import os
from dotenv import load_dotenv
# Create Bearer token reader
security = HTTPBearer()

load_dotenv()

# Create Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

#function to get Token verification from supabase
def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    #extract token from header
    token = cred.credentials
    #verify token with supabase
    user = supabase.auth.get_user(token) #get user details from supabase
    
    #chk invalid token
    if user is None:
        raise HTTPException(status_code=401, detail="invalid token")

    return user

#Make Function for Role check
def check_admin_or_subadmin(user):# It gets user return from get_current_user function
    #Fetch user role from user_roles table
    role_data = supabase.table("user_roles").select("role").eq("user_id", user.user.id).execute()
    #if no role is found 
    if not role_data.data:
        raise HTTPException(status_code=403, detail="Role not found")
    # Get the role
    role = role_data.data[0]['role']
    #Role check for admin and subadmin
    if role_data.data[0]['role'] not in ['admin', 'subadmin']:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins and Subadmins only")

    return role
