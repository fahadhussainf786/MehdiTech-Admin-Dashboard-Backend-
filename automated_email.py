from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
import smtplib
from fastapi import Body
from email.mime.text import MIMEText

load_dotenv()

#smtp server configuration
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")
#Routing for email operations
email_router = APIRouter(prefix="/emails", tags=["emails"])

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

app =FastAPI()
#Create send email function
def send_email(to_email, subject, body):
    print("smtpemail",smtp_email,smtp_password)
    msg =MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_email
    msg["To"] = to_email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, to_email, msg.as_string())

#Automated email sending
@email_router.patch("/applications/{app_id}/status")
def update_application_status(app_id, data: dict = Body(...), user=Depends(get_current_user)):
    try:
        print("start")
        check_admin_or_subadmin(user)
        print("admin checked")
        status = data["status"]
        print("status saved")
        supabase.table("applications").update({"status": status}).eq("id", app_id).execute()
        print("updating the status")
        app_data = supabase.table("applications").select("user_email").eq("id", app_id).single().execute()
        print("getting useremail")
        template = supabase.table("email_templates").select("subject", "body").eq("status", status).single().execute()
        print("getting the template")
        send_email(
            app_data.data["user_email"],
            template.data["subject"],
            template.data["body"]
        )
        print("After getting template send email", send_email)
        
        return {"message": "status updated and email sent"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application status: {str(e)}")

     