# Login, Signup & Blog APIs - FastAPI Backend

A comprehensive FastAPI-based backend system for user authentication, blog management, and job postings with role-based access control and image upload capabilities.

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [File Documentation](#file-documentation)
- [CORS Configuration](#cors-configuration)
- [Authentication & Authorization](#authentication--authorization)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

---

## 🗂️ Project Structure

```
login signup and blog apis/
├── main.py                  # Main FastAPI app & authentication endpoints
├── blog_apis.py             # Blog CRUD endpoints
├── jobs.py                  # Job posting management endpoints
├── auth.py                  # Authentication & role verification utilities
├── cloudinary_utils.py      # Image upload to Cloudinary
├── automated_email.py       # Email notification system
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed)
└── README.md               # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Installation

**1. Navigate to project directory**
```bash
cd "d:\Fastapi projects\login signup and blog apis"
```

**2. Create virtual environment**
```bash
python -m venv venv
```

**3. Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install fastapi uvicorn supabase python-dotenv cloudinary python-multipart
```

**5. Create .env file**
```bash
# Create a new .env file in the root directory
```

**6. Add environment variables** (see [Environment Variables](#environment-variables) section)

**7. Run the development server**
```bash
uvicorn main:app --reload
```

Server will start at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

---

## 🔑 Environment Variables

Create a `.env` file in the root directory with these variables:

```env
# ============= SUPABASE CONFIGURATION =============
SUPABASE_URL=https://your-project-url.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# ============= CLOUDINARY CONFIGURATION =============
# Used for image uploads in blog posts
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ============= EMAIL CONFIGURATION =============
# Used for sending email notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

**Getting Credentials:**
- **Supabase**: https://supabase.com → Create project → Settings → API keys
- **Cloudinary**: https://cloudinary.com → Sign up → Dashboard → API Keys
- **Gmail**: Enable 2FA → Generate App Password

---

## 🔗 API Endpoints

### Base URL
```
Local: http://localhost:8000
Production: https://mehditech-admin-dashboard-backend-production.up.railway.app
```

All responses include proper `Content-Type: application/json` header.

---

### 🔐 Authentication Endpoints (main.py)

#### 1. Sign Up
**Create new user account**

```http
POST /signup
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (201 Created):**
```json
{
  "message": "User has signed up successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Signup failed (user might already exist)
- `500 Internal Server Error`: Server error

---

#### 2. Login
**Authenticate user and get JWT token**

```http
POST /login
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "Role": "admin",
  "email": "user@example.com"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `500 Internal Server Error`: Server error

---

#### 3. Admin Dashboard
**Access admin dashboard (Admin only)**

```http
GET /admin
Authorization: Bearer {access_token}
```

**Success Response (200 OK):**
```json
{
  "message": "Welcome to the admin dashboard"
}
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User is not admin
- `500 Internal Server Error`: Server error

---

### 📝 Blog Endpoints (blog_apis.py)

#### 1. Create Blog
**Create new blog post with optional image**

```http
POST /blogs/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Form Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Blog post title |
| content | string | Yes | Blog post content (HTML allowed) |
| author | string | Yes | Author name |
| tags | string | Yes | Comma-separated tags (e.g., "javascript, web, fastapi") |
| category | string | Yes | Blog category |
| image | file | No | Thumbnail image (jpg, png, gif) |
| internal_images | array | No | Images for blog content |

**Success Response (201 Created):**
```json
{
  "message": "Blog created successfully"
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User is not admin/subadmin
- `500 Internal Server Error`: Server error

---

#### 2. Get All Blogs
**Retrieve all published blogs**

```http
GET /blogs/
```

**Success Response (200 OK):**
```json
{
  "blogs": [
    {
      "id": "uuid-1234-5678",
      "title": "Getting Started with FastAPI",
      "content": "<p>FastAPI is a modern web framework...</p>",
      "author": "John Doe",
      "tags": ["fastapi", "python", "web"],
      "category": "Technology",
      "thumbnail": "https://cloudinary.com/image.jpg",
      "created_at": "2025-01-16T10:30:00Z"
    }
  ]
}
```

---

#### 3. Get Single Blog
**Retrieve a specific blog by ID**

```http
GET /blogs/{blog_id}
```

**Success Response (200 OK):**
```json
{
  "blog": {
    "id": "uuid-1234-5678",
    "title": "Blog Title",
    "content": "<p>Blog content...</p>",
    "author": "John Doe",
    "tags": ["tag1", "tag2"],
    "category": "Category",
    "thumbnail": "https://cloudinary.com/image.jpg"
  }
}
```

**Error Responses:**
- `404 Not Found`: Blog not found
- `500 Internal Server Error`: Server error

---

#### 4. Update Blog
**Update existing blog post (Admin/Subadmin only)**

```http
PUT /blogs/{blog_id}
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "<p>Updated content</p>",
  "image_url": "https://new-image-url.jpg",
  "internal_urls": [],
  "author": "John Doe",
  "tags_list": ["tag1", "tag2"],
  "category": "Updated Category"
}
```

**Success Response (200 OK):**
```json
{
  "message": "Blog updated successfully"
}
```

---

#### 5. Delete Blog
**Delete a blog post (Admin/Subadmin only)**

```http
DELETE /blogs/{blog_id}
Authorization: Bearer {access_token}
```

**Success Response (200 OK):**
```json
{
  "message": "Blog deleted successfully"
}
```

---

### 💼 Job Endpoints (jobs.py)

#### 1. Create Job
**Create new job posting (Admin/Subadmin only)**

```http
POST /jobs/
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Senior Full Stack Developer",
  "department": "Engineering",
  "emp_type": "Full-time",
  "job_des": "We are looking for an experienced Full Stack Developer...",
  "qualifications": "5+ years experience, BS in CS",
  "salary_range": "$80,000 - $120,000",
  "location": "Remote"
}
```

**Success Response (201 Created):**
```json
{
  "message": "Job created successfully"
}
```

---

#### 2. Get All Jobs
**Retrieve all job postings**

```http
GET /jobs/jobs
```

**Success Response (200 OK):**
```json
{
  "data": [
    {
      "id": "job-uuid-1234",
      "title": "Senior Developer",
      "department": "Engineering",
      "employment_type": "Full-time",
      "status": "live"
    }
  ]
}
```

---

#### 3. Get Single Job
**Retrieve specific job by ID**

```http
GET /jobs/jobs/{job_id}
```

**Success Response (200 OK):**
```json
{
  "data": [{ /* job object */ }]
}
```

---

#### 4. Update Job
**Update job details (Admin/Subadmin only)**

```http
PUT /jobs/{job_id}
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Success Response (200 OK):**
```json
{
  "message": "Job updated successfully"
}
```

---

#### 5. Publish Job
**Change job status to "live" (Admin/Subadmin only)**

```http
PATCH /jobs/{job_id}/publish
Authorization: Bearer {access_token}
```

**Success Response (200 OK):**
```json
{
  "message": "Job live successfully"
}
```

---

#### 6. Close Job
**Change job status to "closed" (Admin/Subadmin only)**

```http
PATCH /jobs/{job_id}/close
Authorization: Bearer {access_token}
```

**Success Response (200 OK):**
```json
{
  "message": "Job closed successfully"
}
```

---

#### 7. Delete Job
**Delete job posting (Admin/Subadmin only)**

```http
DELETE /jobs/{job_id}
Authorization: Bearer {access_token}
```

**Success Response (200 OK):**
```json
{
  "message": "Job deleted successfully"
}
```

---

## 📄 File Documentation

### main.py
**Purpose:** Main FastAPI application entry point with authentication endpoints.

**Key Components:**
- CORS Middleware configuration
- User signup endpoint
- User login endpoint with role assignment
- Admin dashboard endpoint

**CORS Configuration:**
```python
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://admin-section-mehdi-tech.vercel.app"
]
```

**Key Functions:**
- `signup(data)` - Register new user
- `login(data)` - Authenticate and return token
- `admin_dashboard(user)` - Admin-only dashboard access

---

### auth.py
**Purpose:** Authentication and authorization utilities.

**Key Functions:**
```python
def get_current_user(cred: HTTPAuthorizationCredentials):
    """Verify JWT token and return user object"""
    
def check_admin_or_subadmin(user):
    """Verify user has admin or subadmin role"""
```

**Usage:**
```python
@app.post("/protected")
def protected_endpoint(user=Depends(get_current_user)):
    check_admin_or_subadmin(user)
    # Proceed with endpoint logic
```

---

### blog_apis.py
**Purpose:** Blog management CRUD endpoints.

**Key Features:**
- Create blogs with image uploads
- Read single or all blogs
- Update blog details
- Delete blogs
- Role-based access control
- Cloudinary image integration

**Endpoints:**
- `POST /blogs/` - Create blog
- `GET /blogs/` - Get all blogs
- `GET /blogs/{blog_id}` - Get single blog
- `PUT /blogs/{blog_id}` - Update blog
- `DELETE /blogs/{blog_id}` - Delete blog

---

### jobs.py
**Purpose:** Job posting management endpoints.

**Key Features:**
- Create job postings (draft status)
- Manage job status (draft → live → closed)
- Full CRUD operations
- Role-based access control

**Job Status Flow:**
```
Created (draft) → Publish → Live → Close → Closed → Delete
```

**Endpoints:**
- `POST /jobs/` - Create job
- `GET /jobs/jobs` - Get all jobs
- `GET /jobs/jobs/{job_id}` - Get single job
- `PUT /jobs/{job_id}` - Update job
- `PATCH /jobs/{job_id}/publish` - Publish job
- `PATCH /jobs/{job_id}/close` - Close job
- `DELETE /jobs/{job_id}` - Delete job

---

## 🔐 CORS Configuration

**Allowed Origins:**
```
http://localhost:5173      # Local Vite frontend
http://127.0.0.1:5173     # Local Vite frontend (IP)
http://localhost:3000      # Local React dev server
https://admin-section-mehdi-tech.vercel.app  # Production
```

**To add a new origin:**
1. Update `origins` list in `main.py`
2. Restart the server

---

## 🔑 Authentication & Authorization

### Bearer Token Format
All protected endpoints require:
```
Authorization: Bearer {access_token}
```

### Role Levels
- `admin` - Full access to all operations
- `subadmin` - Can manage content (blogs, jobs)
- `user` - Limited access (read-only)

---

## 📊 Error Handling

### HTTP Status Codes
| Code | Meaning |
|------|---------|
| 200 | OK - Successful request |
| 201 | Created - Resource created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Unexpected error |

### Error Response Format
```json
{
  "detail": "Error message explaining what went wrong"
}
```

---

## 🛠️ Troubleshooting

### CORS Error
**Error:** Cross-Origin Request Blocked

**Solution:**
1. Verify frontend URL is in `origins` list in `main.py`
2. Restart server after changes

### 401 Unauthorized
**Error:** Invalid token

**Solution:**
- Ensure token is included in headers
- Check token is not expired
- Verify token format: `Authorization: Bearer {token}`

### 403 Forbidden Access
**Error:** Access forbidden

**Solution:**
- Check user role in `user_roles` table
- Ensure role is "admin" or "subadmin"

### Image Upload Fails
**Error:** Image upload failed

**Solution:**
1. Verify Cloudinary credentials in `.env`
2. Check file size < 10MB
3. Ensure format is jpg, png, or gif

---

## 🚀 Deployment

### Deploy to Railway

**1. Push Code to GitHub**
**2. Connect to Railway dashboard**
**3. Set Environment Variables**
**4. Deploy**

**Production URL:**
```
https://mehditech-admin-dashboard-backend-production.up.railway.app
```

---

## 💡 Frontend Integration Tips

### Content-Type Headers
**For JSON requests:**
```javascript
headers: {
  'Content-Type': 'application/json'
}
```

**For file uploads (do NOT set manually):**
```javascript
// Browser automatically sets Content-Type: multipart/form-data
const formData = new FormData();
// Add fields...
fetch(url, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
    // Do NOT set Content-Type
  },
  body: formData
})
```

---

**Last Updated:** January 16, 2026

2. Create a `.env` file with the following variables:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   Cloudinary_CLOUD_NAME=your_cloudinary_cloud_name
   Cloudinary_API_KEY=your_cloudinary_api_key
   Cloudinary_API_SECRET=your_cloudinary_api_secret
   ```

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

## Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header as `Bearer <token>`.

## API Endpoints

### Authentication Endpoints

#### POST /signup
Sign up a new user.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
- 200: `{"message": "User has signed up successfully"}`
- 400: `{"detail": "Signup failed"}`

#### POST /login
Log in an existing user.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
- 200: `{"access_token": "string", "token_type": "bearer", "Role": "string", "email": "string"}`
- 401: `{"detail": "invalid credentials"}`

#### GET /admin
Access the admin dashboard (requires admin role).

**Headers:**
- Authorization: Bearer <token>

**Response:**
- 200: `{"message": "Welcome to the admin dashboard"}`
- 401: `{"detail": "invalid token"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access for Admins only"}`

### Blog Endpoints

All blog endpoints require authentication with admin or subadmin role.

#### POST /blogs/
Create a new blog post.

**Headers:**
- Authorization: Bearer <token>

**Form Data:**
- title: string (required)
- content: string (required)
- author: string (required)
- tags: string (comma-separated, required)
- category: string (required)
- image: file (required, thumbnail image)
- internal_images: files (optional, list of images for content)

**Response:**
- 200: `{"message": "Blog created successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### GET /blogs/
Get all blog posts.

**Headers:**
- Authorization: Bearer <token>

**Response:**
- 200: `{"blogs": [array of blog objects]}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### GET /blogs/{blog_id}
Get a specific blog post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- blog_id: string

**Response:**
- 200: `{"blog": blog object}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`
- 404: `{"detail": "Blog not found"}`

#### PUT /blogs/{blog_id}
Update an existing blog post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- blog_id: string

**Request Body:**
```json
{
  "title": "string",
  "content": "string",
  "image_url": "string",
  "internal_urls": "array",
  "author": "string",
  "tags_list": "array",
  "category": "string"
}
```

**Response:**
- 200: `{"message": "Blog updated successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### DELETE /blogs/{blog_id}
Delete a blog post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- blog_id: string

**Response:**
- 200: `{"message": "Blog deleted successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

### Job Endpoints

All job endpoints require authentication with admin or subadmin role.

#### POST /jobs/
Create a new job post.

**Headers:**
- Authorization: Bearer <token>

**Request Body:**
```json
{
  "title": "string",
  "role_description": "string",
  "responsibilities": "string (optional)",
  "requirements": "string (optional)",
  "salary_min": "number (optional)",
  "salary_max": "number (optional)",
  "location": "string (optional)"
}
```

**Response:**
- 200: Job data
- 400: `{"detail": "Missing fields"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### GET /jobs/jobs/{job_id}
Get a specific job post.

**Path Parameters:**
- job_id: string

**Response:**
- 200: Job data

#### GET /jobs/jobs
Get all job posts.

**Response:**
- 200: Array of job objects

#### PUT /jobs/{job_id}
Update an existing job post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- job_id: string

**Request Body:**
```json
{
  "title": "string",
  "role_description": "string",
  "responsibilities": "string",
  "requirements": "string",
  "salary_min": "number",
  "salary_max": "number",
  "location": "string",
  "status": "string"
}
```

**Response:**
- 200: Updated job data
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`
- 404: `{"detail": "Job not found"}`

#### PATCH /jobs/{job_id}/publish
Publish a job post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- job_id: string

**Response:**
- 200: `{"message": "Job live successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### PATCH /jobs/{job_id}/close
Close a job post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- job_id: string

**Response:**
- 200: `{"message": "Job closed successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

#### DELETE /jobs/{job_id}
Delete a job post.

**Headers:**
- Authorization: Bearer <token>

**Path Parameters:**
- job_id: string

**Response:**
- 200: `{"message": "Job deleted successfully"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins and Subadmins only"}`

## Database Schema

### user_roles table
- user_id: string
- role: string (admin, subadmin, user, etc.)

### blogs table
- id: string (auto-generated)
- title: string
- content: string
- thumbnail: string (Cloudinary URL)
- internal_urls: array of strings (Cloudinary URLs)
- created_by: string (user ID)
- author: string
- tags: array of strings
- category: string

### jobs table
- id: string (auto-generated)
- title: string
- role_description: string
- responsibilities: string
- requirements: string
- salary_min: number
- salary_max: number
- location: string
- status: string (draft, live, closed)

## Notes

- Image uploads are handled via Cloudinary.
- Roles are checked against the `user_roles` table in Supabase.
- Blog and job operations require admin or subadmin privileges.
- The application uses Supabase for authentication and database operations.
- CORS is enabled for localhost origins.
