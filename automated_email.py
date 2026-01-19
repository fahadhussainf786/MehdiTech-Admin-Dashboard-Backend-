from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.security import HTTPBearer
from supabase import create_client
import os
from dotenv import load_dotenv
from auth import get_current_user, check_admin_or_subadmin
import smtplib
from fastapi import Body
from email.mime.text import MIMEText

#smtp server configuration
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")

load_dotenv()
#Routing for email operations
email_router = APIRouter(prefix="/emails", tags=["emails"])

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

app =FastAPI()
#Create send email function
def send_email(to_email, subject, body):
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
def update_application_status(app_id, data: dict= Body(...)):
     
     check_admin_or_subadmin()
     #Get the data from parameter
     status = data["status"]
     #updating the application status and sending the email
     supabase.table("applications").update({"status":status}).eq("id", app_id).execute()
     #Get user_email and verify application data to send email
     app_data = supabase.table("applications").select("user_email").eq("id", app_id ).single().execute()
     #Get email template data
     template = supabase.table("email_templates").select("subject", "body").eq("status", status).single().execute()
     #Send_email function call to send email
     send_email(
         app_data.data["user_email"],
         template.data["subject"],
         template.data["body"]
     )

     return {"message": "status updated and email sent"}
     
     

     