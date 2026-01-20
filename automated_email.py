from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
import asyncio
from fastapi import Body
import resend

load_dotenv()

# Resend configuration
resend.api_key = os.getenv("RESEND_API_KEY")
resend_from_email = os.getenv("RESEND_FROM_EMAIL")
#Routing for email operations
email_router = APIRouter(prefix="/emails", tags=["emails"])

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

app =FastAPI()
#Create async send email function with Resend
async def send_email(to_email, subject, body):
    def send_resend():
        response = resend.Emails.send({
            "from": resend_from_email,
            "to": to_email,
            "subject": subject,
            "html": body  # body from Supabase is HTML
        })
        return response
    
    try:
        response = await asyncio.to_thread(send_resend)
        if response.get("id") is None:
            raise Exception(f"Resend error: {response}")
    except Exception as e:
        print(f"ERROR in send_email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

#Automated email sending
@email_router.patch("/applications/{app_id}/status")
async def update_application_status(app_id, data: dict = Body(...), user=Depends(get_current_user)):
    try:
        check_admin_or_subadmin(user)
        status = data["status"]
        
        supabase.table("applications").update({"status": status}).eq("id", app_id).execute()
        app_data = supabase.table("applications").select("user_email").eq("id", app_id).single().execute()
        template = supabase.table("email_templates").select("subject", "body").eq("status", status).single().execute()
        
        await send_email(
            app_data.data["user_email"],
            template.data["subject"],
            template.data["body"]
        )
        
        return {"message": "status updated and email sent"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application status: {str(e)}")

     