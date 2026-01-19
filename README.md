# Login, Signup & Blog APIs — FastAPI Backend

Comprehensive FastAPI backend providing authentication, role-based access control, blog management with image uploads to Cloudinary, job postings, and automated email notifications.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Requirements & Setup](#requirements--setup)
3. [Environment Variables](#environment-variables)
4. [How to Run](#how-to-run)
5. [CORS Configuration](#cors-configuration)
6. [File Documentation](#file-documentation)
7. [API Reference](#api-reference)
8. [Authentication & Authorization](#authentication--authorization)
9. [Error Handling](#error-handling)
10. [Troubleshooting](#troubleshooting)

---

## Project Structure

```
login signup and blog apis/
├── main.py                  # FastAPI app initialization, CORS, auth endpoints (signup, login, admin)
├── blog_apis.py             # Blog router: create, read, update, delete blogs with image uploads
├── jobs.py                  # Jobs router: create, read, update, delete job postings
├── auth.py                  # Authentication utilities: token verification, role checks
├── cloudinary_utils.py      # Cloudinary configuration and image upload helper
├── automated_email.py       # Email router: send automated emails for application status updates
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed to version control)
└── README.md               # This documentation file
```

---

## Requirements & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (strongly recommended)

### Installation

1. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

   Or individually:
   ```powershell
   pip install fastapi uvicorn supabase python-dotenv cloudinary python-multipart
   ```

---

## Environment Variables

Create a `.env` file in the project root with the following variables (use exact names):

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Cloudinary Configuration (note: camel-case names)
Cloudinary_CLOUD_NAME=your_cloud_name
Cloudinary_API_KEY=your_api_key
Cloudinary_API_SECRET=your_api_secret

# Email Configuration (SMTP)
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Getting Credentials
- **Supabase**: https://supabase.com → Create project → Settings → API Keys
- **Cloudinary**: https://cloudinary.com → Dashboard → API Keys
- **Gmail SMTP**: Enable 2FA → Generate App Password (use app-specific password, not main Gmail password)

---

## How to Run

Start the development server:

```powershell
uvicorn main:app --reload
```

**Server runs at:** `http://localhost:8000`
**API Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)
**Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)

---

## CORS Configuration

The application uses `CORSMiddleware` configured in `main.py`.

**Origins List (in `main.py`):**
```python
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://admin-section-mehdi-tech.vercel.app"
]
```

**To add your frontend origin:**
1. Add the exact frontend URL to the `origins` list in `main.py`
2. Restart the server
3. **Important:** Use exact URL (no trailing slash). Example: `https://example.com` not `https://example.com/`

**Request Requirements for CORS:**
- Include `Origin` header in requests (browser does this automatically)
- For multipart file uploads: send `Content-Type: multipart/form-data` (let the HTTP client set the boundary, don't set manually)
- For protected endpoints: include `Authorization: Bearer {access_token}` header

---

## File Documentation

### 1. **main.py** — FastAPI App & Authentication

**Purpose:** Application initialization, CORS setup, and user authentication endpoints.

**Key Components:**

#### CORSMiddleware Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

#### Global Exception Handler
Catches all unhandled exceptions and returns CORS-compliant error responses:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception)
```
- Returns 500 status with error detail
- Includes `Access-Control-Allow-Origin` header to prevent CORS blocking

#### Supabase Client
```python
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
```
Used for all database operations and user authentication.

#### Endpoints

**POST /signup**
- Create new user account in Supabase Auth
- Request Body: `{ "email": "user@example.com", "password": "password123" }`
- Response (success): `{ "message": "User has signed up successfully" }`
- Status Codes: 200 (success), 400 (signup failed), 500 (server error)

**POST /login**
- Authenticate user and return JWT token
- Request Body: `{ "email": "user@example.com", "password": "password123" }`
- Response (success): 
  ```json
  {
    "access_token": "eyJhbGci...",
    "token_type": "bearer",
    "Role": "admin",
    "email": "user@example.com"
  }
  ```
- Status Codes: 200 (success), 401 (invalid credentials), 500 (server error)
- **Note:** Role is fetched from `user_roles` table in Supabase

**GET /admin**
- Protected endpoint (requires valid token)
- Authorization: `Authorization: Bearer {access_token}`
- Response (success): `{ "message": "Welcome to the admin dashboard" }`
- Status Codes: 200 (success), 401 (missing/invalid token), 403 (user not admin), 500 (server error)
- **Note:** Only allows users with role 'admin'

#### Router Includes
- `blog_router` from `blog_apis.py` (prefix: `/blogs`)
- `jobs_router` from `jobs.py` (prefix: `/jobs`)
- `email_router` from `automated_email.py` (prefix: `/emails`)

---

### 2. **blog_apis.py** — Blog Management

**Purpose:** CRUD operations for blog posts with image upload capabilities.

**Router:** Mounted at `/blogs`

**Dependencies:**
- Supabase for database operations
- Cloudinary for image storage
- Authentication: `get_current_user`, `check_admin_or_subadmin`

**Endpoints:**

**POST /blogs/uploadimage**
- Helper endpoint for uploading single images
- Form Data: `image_file` (file)
- Response: `"https://cloudinary-secure-url.jpg"`
- Used internally by create_blog

**POST /blogs/**
- Create new blog post (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Content-Type: `multipart/form-data`
- Form Fields:
  - `title` (string, required) — Blog post title
  - `content` (string, required) — Blog content (HTML supported)
  - `author` (string, required) — Author name
  - `tags` (string, required) — Comma-separated tags (e.g., "python, fastapi, web")
  - `category` (string, required) — Blog category
  - `image` (file, optional) — Thumbnail image
  - `internal_images` (file[], optional) — Multiple images for blog content
- Response (success): `{ "message": "Blog created successfully" }`
- Error Handling:
  - 400: Thumbnail upload failed / Internal image upload failed / DB insert failed
  - 401: Invalid/missing token
  - 403: User is not admin/subadmin
  - 500: Unexpected server error
- Database: Inserts record into `blogs` table with uploaded URLs and user ID

**GET /blogs/**
- Retrieve all blogs (no authentication required)
- Response: `{ "blogs": [{ id, title, content, thumbnail, ... }, ...] }`
- Status Codes: 200 (success), 500 (server error)

**GET /blogs/{blog_id}**
- Retrieve single blog by ID (no authentication required)
- Response (success): `{ "blog": { id, title, content, ... } }`
- Status Codes: 200 (success), 404 (blog not found), 500 (server error)

**PUT /blogs/{blog_id}**
- Update blog post (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Content-Type: `application/json`
- Request Body:
  ```json
  {
    "title": "Updated Title",
    "content": "<p>Updated content</p>",
    "image_url": "https://new-thumbnail-url.jpg",
    "internal_urls": ["url1", "url2"],
    "author": "John Doe",
    "tags_list": ["tag1", "tag2"],
    "category": "Updated Category"
  }
  ```
- Response (success): `{ "message": "Blog updated successfully" }`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)

**DELETE /blogs/{blog_id}**
- Delete blog post (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Response (success): `{ "message": "Blog deleted successfully" }`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)

**Error Handling:**
- Image uploads wrapped in try/except with specific error messages
- Database insert wrapped in try/except
- HTTPException re-raised to preserve status codes
- Unexpected exceptions converted to 500 errors

---

### 3. **jobs.py** — Job Postings Management

**Purpose:** CRUD operations for job postings.

**Router:** Mounted at `/jobs`

**Dependencies:**
- Supabase for database operations
- Authentication: `get_current_user`, `check_admin_or_subadmin`

**Endpoints:**

**POST /jobs/**
- Create new job posting (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Content-Type: `application/json`
- Request Body:
  ```json
  {
    "title": "Senior Full Stack Developer",
    "department": "Engineering",
    "emp_type": "Full-time",
    "job_des": "Job description...",
    "qualifications": "Required qualifications...",
    "salary_range": "$80,000 - $120,000",
    "location": "Remote"
  }
  ```
- Response (success): `[{ id, title, department, ... }]`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)
- Database: Inserts record into `jobs` table with status set to "live"

**GET /jobs/jobs**
- Retrieve all job postings (no authentication required)
- Response: `[{ id, title, department, emp_type, status, ... }, ...]`
- Status Codes: 200 (success), 500 (server error)

**GET /jobs/jobs/{job_id}**
- Retrieve single job by ID (no authentication required)
- Response: `[{ id, title, department, ... }]`
- Status Codes: 200 (success), 500 (server error)

**PUT /jobs/{job_id}**
- Update job posting (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Content-Type: `application/json`
- Request Body: Updated job fields (title, department, emp_type, job_des, etc.)
- Response (success): Updated job record
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 404 (job not found), 500 (server error)

**PATCH /jobs/{job_id}/close**
- Mark job as closed (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Response (success): `{ "message": "Job closed successfully" }`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)
- Database: Updates `jobs` record with `status` = "closed"

**DELETE /jobs/{job_id}**
- Delete job posting (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Response (success): `{ "message": "Job deleted successfully" }`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)

**Error Handling:**
- Role checks via `check_admin_or_subadmin(user)` raise 403 HTTPException
- HTTPException re-raised to preserve status codes
- Unexpected exceptions converted to 500 errors with description

---

### 4. **auth.py** — Authentication & Authorization

**Purpose:** Token verification and role-based access control utilities.

**Dependencies:**
- Supabase for user verification
- FastAPI HTTPBearer for token extraction

**Key Functions:**

**get_current_user(cred: HTTPAuthorizationCredentials)**
- Extract and verify JWT token from Authorization header
- Parameter: HTTP Bearer credentials (automatically extracted by FastAPI)
- Returns: User object from Supabase
- Raises: `HTTPException(401, "invalid token")` if token is invalid
- Usage: Use as dependency in protected endpoints
- Example:
  ```python
  @app.get("/protected")
  def protected_endpoint(user=Depends(get_current_user)):
      return {"user_id": user.user.id}
  ```

**check_admin_or_subadmin(user)**
- Verify user has admin or subadmin role
- Parameter: User object (from `get_current_user`)
- Returns: Role string ("admin" or "subadmin")
- Raises: 
  - `HTTPException(403, "Role not found")` if user has no role in `user_roles` table
  - `HTTPException(403, "Access forbidden: Admins and Subadmins only")` if role is neither admin nor subadmin
- Usage: Call in protected endpoints before performing admin-only operations
- Example:
  ```python
  @app.post("/admin-action")
  def admin_action(user=Depends(get_current_user)):
      check_admin_or_subadmin(user)  # Raises 403 if not admin/subadmin
      # Proceed with admin operation
  ```

**Supabase Tables Required:**
- `user_roles` — Must have columns: `user_id`, `role`
  - Valid roles: "admin", "subadmin", "user"

---

### 5. **cloudinary_utils.py** — Image Upload Configuration

**Purpose:** Cloudinary configuration and image upload helper function.

**Configuration:**
- Uses environment variables: `Cloudinary_CLOUD_NAME`, `Cloudinary_API_KEY`, `Cloudinary_API_SECRET`
- Initializes Cloudinary SDK on module import

**Key Function:**

**upload_image(image_file)**
- Upload image file to Cloudinary
- Parameter: `image_file` (file object from FastAPI UploadFile or file handle)
- Returns: Secure URL string from Cloudinary
- Raises: Exception if upload fails (e.g., invalid file, API error)
- Example:
  ```python
  from cloudinary_utils import upload_image
  url = upload_image(file_object)  # Returns "https://res.cloudinary.com/..."
  ```

**Error Handling:**
- If Cloudinary upload fails, exception is caught by endpoint handler and returns 400 status
- Error message includes descriptive details from Cloudinary

---

### 6. **automated_email.py** — Automated Email Notifications

**Purpose:** Send automated emails for application status updates.

**Router:** Mounted at `/emails`

**Dependencies:**
- Supabase for database queries and status updates
- SMTP (Gmail) for email sending
- Authentication: `get_current_user`, `check_admin_or_subadmin`

**Configuration:**
- SMTP Server: `smtp.gmail.com`
- SMTP Port: 587
- Uses environment variables: `SMTP_EMAIL`, `SMTP_PASSWORD`

**Key Function:**

**send_email(to_email, subject, body)**
- Send email via SMTP
- Parameters:
  - `to_email` (string) — Recipient email address
  - `subject` (string) — Email subject line
  - `body` (string) — Email body/content
- No return value (sends directly via SMTP)
- Raises: Exception if SMTP connection/sending fails

**Endpoints:**

**PATCH /emails/applications/{app_id}/status**
- Update application status and send email notification (Admin/Subadmin only)
- Authorization: `Authorization: Bearer {access_token}`
- Content-Type: `application/json`
- Request Body:
  ```json
  {
    "status": "approved"
  }
  ```
- Supported statuses: "approved", "rejected", "pending", "under_review" (or other statuses that exist in `email_templates` table)
- Response (success): `{ "message": "status updated and email sent" }`
- Status Codes: 200 (success), 401 (invalid token), 403 (not authorized), 500 (server error)

**Database Operations:**
1. Updates `applications` table: sets `status` field for given `app_id`
2. Fetches recipient email from `applications` table: `user_email` field
3. Fetches email template from `email_templates` table: matches `status` field to get `subject` and `body`
4. Sends email with template subject and body

**Supabase Tables Required:**
- `applications` — Columns: `id`, `user_email`, `status`
- `email_templates` — Columns: `status`, `subject`, `body`

**SMTP Requirements:**
- Gmail account with 2FA enabled
- App-specific password generated (use this in SMTP_PASSWORD, not main Gmail password)

---

## API Reference

### Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Status Codes Summary

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid input, file upload failed, DB insert failed |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | User role does not permit this action |
| 404 | Not Found | Requested resource does not exist |
| 500 | Internal Server Error | Unexpected server error |

### Common Headers

**Request Headers (all protected endpoints):**
```
Authorization: Bearer {access_token}
```

**Request Headers (multipart file upload):**
```
Content-Type: multipart/form-data
```
(Browser/client sets this automatically when using FormData; do not set manually)

**Request Headers (JSON):**
```
Content-Type: application/json
```

**Response Headers (all endpoints):**
```
Content-Type: application/json
Access-Control-Allow-Origin: {frontend_origin}
Access-Control-Allow-Credentials: true
```

---

## Authentication & Authorization

### Token Flow

1. **User Signs Up:** POST `/signup` → Account created in Supabase Auth
2. **User Logs In:** POST `/login` → Returns `access_token` and user role
3. **Use Token:** Include `Authorization: Bearer {access_token}` in protected requests
4. **Token Verification:** Server verifies token with Supabase on each protected request

### Role-Based Access Control

**Roles:**
- `admin` — Full access to all operations
- `subadmin` — Access to admin-level operations (same as admin in current implementation)
- `user` — Limited access (cannot create/update/delete)

**Protected Endpoints Requiring Admin/Subadmin:**
- POST /blogs/ (create blog)
- PUT /blogs/{blog_id} (update blog)
- DELETE /blogs/{blog_id} (delete blog)
- POST /jobs/ (create job)
- PUT /jobs/{job_id} (update job)
- PATCH /jobs/{job_id}/close (close job)
- DELETE /jobs/{job_id} (delete job)
- PATCH /emails/applications/{app_id}/status (update status & send email)
- GET /admin (admin dashboard)

**Protected Endpoints Requiring Valid Token (any role):**
- Any endpoint that requires `Depends(get_current_user)`

### User Role Management

User roles are stored in the `user_roles` table in Supabase:

```
user_roles
├── user_id (UUID, references auth.users)
├── role (string: "admin", "subadmin", or "user")
└── created_at (timestamp)
```

To assign roles:
1. After user signup, manually add record to `user_roles` table
2. Set `user_id` to the newly created user's ID (from Supabase Auth)
3. Set `role` to desired role

---

## Error Handling

### Error Handling Strategy

The backend uses a layered error handling approach:

1. **Specific Errors** — Caught and converted to meaningful HTTP status codes
   - 400 for validation, upload, and database errors
   - 403 for authorization failures
   - 404 for missing resources

2. **Preserved Errors** — HTTPException status codes are re-raised as-is
   - Maintains proper status codes from role checks
   - Example: `check_admin_or_subadmin` raises 403, which is re-raised

3. **Unexpected Errors** — Converted to 500 with error detail
   - Outer try/except catches unexpected exceptions
   - Returns 500 status with error message

4. **Global Handler** — Catches any unhandled exceptions
   - Ensures CORS headers are included in error responses
   - Prevents browser from blocking error responses

### Example Error Flow (Blog Creation)

```
POST /blogs/
  ├─ check_admin_or_subadmin(user) → 403 if not admin/subadmin (re-raised)
  ├─ upload thumbnail image → 400 if upload fails (caught, re-raised as 400)
  ├─ upload internal images → 400 if any upload fails (caught, re-raised as 400)
  ├─ insert into database → 400 if DB insert fails (caught, re-raised as 400)
  └─ unexpected error → 500 (caught by outer handler, converted to 500)
```

---

## Troubleshooting

### CORS Error: "Access-Control-Allow-Origin missing"

**Causes:**
- Frontend origin not in `origins` list in `main.py`
- Frontend origin includes trailing slash (must match exactly)
- Server not restarted after adding origin

**Solution:**
1. Verify frontend origin in browser developer tools (Network tab, Request headers)
2. Add exact origin to `origins` list in `main.py` (e.g., `https://example.com` not `https://example.com/`)
3. Restart the server: `uvicorn main:app --reload`

### File Upload Returns 400 Error

**Causes:**
- Frontend setting `Content-Type: multipart/form-data` manually (incorrect)
- File upload parameter name mismatch (should be `image` for thumbnail, `internal_images` for blog images)
- Cloudinary credentials invalid or expired

**Solution:**
1. Use browser's FormData API or equivalent (let it set Content-Type automatically)
2. Verify field names match endpoint parameters in `blog_apis.py`
3. Check `.env` Cloudinary credentials match your Cloudinary account
4. Check error message returned from API for specific Cloudinary error

### Authorization Error: "invalid token" (401)

**Causes:**
- Authorization header not included
- Token format incorrect (should be `Bearer {token}`, not just `{token}`)
- Token expired or invalid

**Solution:**
1. Ensure header: `Authorization: Bearer {access_token}` (exact format)
2. Use token from `/login` response
3. Generate new token if old one expired

### Authorization Error: "Access forbidden" (403)

**Causes:**
- User role is not admin or subadmin
- User has no role assigned in `user_roles` table

**Solution:**
1. Assign admin or subadmin role to user in Supabase `user_roles` table
2. Verify `user_id` matches authenticated user's ID
3. Test with admin account

### Email Not Sending

**Causes:**
- SMTP credentials incorrect in `.env`
- Gmail app password not generated (using main Gmail password)
- SMTP_PASSWORD has special characters not properly escaped

**Solution:**
1. Verify `SMTP_EMAIL` and `SMTP_PASSWORD` in `.env`
2. For Gmail: Generate app-specific password (https://myaccount.google.com/apppasswords)
3. Use app password in `SMTP_PASSWORD`, not main Gmail password
4. Test SMTP connection independently if needed

### Database Errors (404, Failed to insert)

**Causes:**
- Supabase table doesn't exist
- Required columns missing from table
- Foreign key constraints not met
- Row doesn't exist for update/delete

**Solution:**
1. Verify Supabase tables exist and have required columns
2. Check Supabase documentation for table schemas
3. Verify required data exists before trying to update/delete
4. Check error message returned from API for specific database error

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] Update `origins` in `main.py` with production frontend URL
- [ ] Update `.env` with production Supabase credentials
- [ ] Update `.env` with production Cloudinary credentials
- [ ] Update `.env` with production SMTP credentials
- [ ] Ensure `SUPABASE_SERVICE_ROLE_KEY` is kept secret (environment variable, not in code)
- [ ] Set FastAPI debug mode to False in production
- [ ] Use production ASGI server (e.g., Gunicorn) instead of development uvicorn

### Recommended Deployment Platforms

- Railway (currently in `origins`)
- Render
- Fly.io
- AWS EC2 / Elastic Beanstalk

---

## Support & Debugging

For additional help:
1. Check FastAPI documentation: https://fastapi.tiangolo.com
2. Check Supabase documentation: https://supabase.com/docs
3. Check Cloudinary documentation: https://cloudinary.com/documentation
4. Review server logs: Check uvicorn output for error details
5. Use FastAPI Swagger UI (`/docs`) to test endpoints interactively

