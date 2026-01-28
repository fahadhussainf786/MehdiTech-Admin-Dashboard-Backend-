# FastAPI Backend - Login, Signup, Blog & Job Management System

A comprehensive FastAPI backend API providing user authentication, role-based access control, blog management with image uploads, job postings, and automated email notifications.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Environment Configuration](#environment-configuration)
- [API Endpoints](#api-endpoints)
- [Authentication & Authorization](#authentication--authorization)
- [Database Schema](#database-schema)
- [Image Upload Configuration](#image-upload-configuration)
- [Email Configuration](#email-configuration)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [CORS Configuration](#cors-configuration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## 🎯 Project Overview

This FastAPI backend provides a complete solution for managing a content management system with the following capabilities:

- **User Authentication**: Secure signup and login with JWT tokens
- **Role-Based Access Control**: Admin, Subadmin, and User roles
- **Blog Management**: Full CRUD operations with image uploads
- **Job Postings**: Create, manage, and track job listings
- **Job Applications**: User application system with resume uploads
- **Automated Emails**: Status update notifications via SMTP
- **Cloud Storage**: Image uploads to Cloudinary
- **File Storage**: Resume uploads to Supabase storage

## ✨ Features

### 🔐 Authentication & Authorization
- User registration and login
- JWT token-based authentication
- Role-based access control (Admin, Subadmin, User)
- Protected endpoints with middleware

### 📝 Blog Management
- Create, read, update, delete blog posts
- Image upload for thumbnails and content
- Tag-based categorization
- Sort blogs by creation date (latest/oldest)
- Admin/Subadmin only editing capabilities

### 💼 Job Management
- Create and manage job postings
- Job status tracking (live/closed)
- Department and location categorization
- Admin/Subadmin only management

### 📋 Job Applications
- User job application system
- Resume upload functionality
- Application status tracking
- Admin application management

### 📧 Automated Email System
- Status change notifications
- SMTP integration with Gmail
- Template-based email content
- Admin-triggered email sending

### ☁️ Cloud Integration
- Cloudinary for image storage
- Supabase for database and file storage
- Secure file upload handling

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running the application

### Database & Storage
- **Supabase** - PostgreSQL database with authentication
- **Cloudinary** - Cloud-based image storage and management

### Authentication & Security
- **JWT Tokens** - Secure authentication
- **HTTP Bearer** - Token-based authorization
- **CORS** - Cross-origin resource sharing

### Email & Utilities
- **SMTP** - Email sending via Gmail
- **Python-dotenv** - Environment variable management
- **Cloudinary SDK** - Image upload utilities
- **Python-multipart** - Form data parsing for file uploads
- **Pydantic** - Data validation and serialization
- **Pydantic-core** - Core validation engine
- **Email-validator** - Email validation utilities
- **Python-http-client** - HTTP client for email services
- **Resend** - Email service integration

## 📁 Project Structure

```
login signup and blog apis/
├── main.py                  # FastAPI app initialization, CORS, auth endpoints
├── auth.py                  # Authentication utilities and role checking
├── blog_apis.py             # Blog management endpoints with image uploads
├── jobs.py                  # Job posting management endpoints
├── applicant_job_apply.py   # Job application system endpoints
├── automated_email.py       # Email notification system
├── cloudinary_utils.py      # Cloudinary configuration and utilities
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This documentation file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "login signup and blog apis"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env
   ```

5. **Configure environment variables** (see [Environment Configuration](#environment-configuration))

6. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## ⚙️ Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Cloudinary Configuration
Cloudinary_CLOUD_NAME=your_cloud_name
Cloudinary_API_KEY=your_api_key
Cloudinary_API_SECRET=your_api_secret

# Email Configuration (SMTP)
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### Getting Credentials

#### Supabase
1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Navigate to Settings → API
4. Copy the Project URL and Service Role Key

#### Cloudinary
1. Go to [Cloudinary](https://cloudinary.com)
2. Create a free account
3. Navigate to Dashboard → Account Details
4. Copy Cloud Name, API Key, and API Secret

#### Gmail SMTP
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → App passwords
3. Generate an app password for "Mail"
4. Use this app password (not your main Gmail password)

## 🌐 API Endpoints

### Authentication Endpoints

#### POST /signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "User has signed up successfully"
}
```

#### POST /login
Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "Role": "admin",
  "email": "user@example.com"
}
```

#### GET /admin
Protected admin dashboard endpoint.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Welcome to the admin dashboard"
}
```

### Blog Management Endpoints

#### POST /blogs/uploadimage
Upload a single image to Cloudinary.

**Form Data:**
- `image_file`: File upload

**Response (200):**
```json
{
  "url": "https://res.cloudinary.com/your-cloud-name/image/upload/..."
}
```

#### POST /blogs/
Create a new blog post (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Form Data:**
- `title`: Blog title
- `content`: Blog content (HTML supported)
- `author`: Author name
- `tags`: Comma-separated tags
- `category`: Blog category
- `image`: Thumbnail image (optional)
- `internal_images`: Internal content images (optional, multiple)

**Response (200):**
```json
{
  "message": "Blog created successfully"
}
```

#### GET /blogs/
Retrieve all blogs (no sorting parameter available in current implementation).

**Response (200):**
```json
{
  "blogs": [
    {
      "id": "uuid",
      "title": "Blog Title",
      "content": "Blog content...",
      "thumbnail": "https://...",
      "internal_urls": ["https://..."],
      "author": "Author Name",
      "tags": ["tag1", "tag2"],
      "category": "Category",
      "created_at": "2023-01-01T00:00:00Z",
      "created_by": "user-id"
    }
  ]
}
```

#### GET /blogs/{blog_id}
Retrieve a specific blog post.

**Response (200):**
```json
{
  "blog": {
    "id": "uuid",
    "title": "Blog Title",
    "content": "Blog content...",
    "thumbnail": "https://...",
    "internal_urls": ["https://..."],
    "author": "Author Name",
    "tags": ["tag1", "tag2"],
    "category": "Category",
    "created_at": "2023-01-01T00:00:00Z",
    "created_by": "user-id"
  }
}
```

#### PUT /blogs/{blog_id}
Update a blog post (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content...",
  "image_url": "https://new-thumbnail-url.jpg",
  "internal_urls": ["url1", "url2"],
  "author": "Updated Author",
  "tags_list": ["tag1", "tag2"],
  "category": "Updated Category"
}
```

#### DELETE /blogs/{blog_id}
Delete a blog post (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Blog deleted successfully"
}
```

### Job Management Endpoints

#### POST /jobs/
Create a new job posting (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Senior Developer",
  "department": "Engineering",
  "emp_type": "Full-time",
  "job_des": "Job description...",
  "qualifications": "Required qualifications...",
  "salary_range": "$80,000 - $120,000",
  "location": "Remote"
}
```

**Response (200):**
```json
[{
  "id": "uuid",
  "title": "Senior Developer",
  "department": "Engineering",
  "employment_type": "Full-time",
  "job_description": "Job description...",
  "qualifications": "Required qualifications...",
  "salary_range": "$80,000 - $120,000",
  "location": "Remote",
  "status": "live",
  "created_at": "2023-01-01T00:00:00Z"
}]
```

#### GET /jobs/jobs
Retrieve all job postings.

**Response (200):**
```json
[{
  "id": "uuid",
  "title": "Senior Developer",
  "department": "Engineering",
  "employment_type": "Full-time",
  "job_description": "Job description...",
  "qualifications": "Required qualifications...",
  "salary_range": "$80,000 - $120,000",
  "location": "Remote",
  "status": "live",
  "created_at": "2023-01-01T00:00:00Z"
}]
```

#### GET /jobs/jobs/{job_id}
Retrieve a specific job posting.

**Response (200):**
```json
[{
  "id": "uuid",
  "title": "Senior Developer",
  "department": "Engineering",
  "employment_type": "Full-time",
  "job_description": "Job description...",
  "qualifications": "Required qualifications...",
  "salary_range": "$80,000 - $120,000",
  "location": "Remote",
  "status": "live",
  "created_at": "2023-01-01T00:00:00Z"
}]
```

#### PUT /jobs/{job_id}
Update a job posting (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Updated Job Title",
  "emp_type": "Part-time",
  "job_des": "Updated description...",
  "salary_range": "Updated range"
}
```

#### PATCH /jobs/{job_id}/close
Close a job posting (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Job closed successfully"
}
```

#### DELETE /jobs/{job_id}
Delete a job posting (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Job deleted successfully"
}
```

### Job Application Endpoints

#### POST /jobapply/job_apply/{job_id}
Apply for a job position.

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

**Form Data:**
- `user_email`: Applicant email
- `title`: Job title (retrieved from job_id)
- `name`: Applicant name
- `phone_number`: Phone number (optional)
- `resume`: Resume file (optional, PDF)

**Response (200):**
```json
{
  "message": "Application submitted successfully",
  "application_id": "uuid"
}
```

#### GET /jobapply/{job_id}/applicants/count
Get total number of applicants for a job.

**Response (200):**
```json
{
  "total applicants": 5
}
```

#### GET /jobapply/my_applications
Get all applications (Admin only - no user filtering in current implementation).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "applications": [
    {
      "id": "uuid",
      "applicant_name": "Applicant Name",
      "user_email": "user@example.com",
      "status": "Applied",
      "created_at": "2023-01-01T00:00:00Z",
      "jobs": {
        "title": "Job Title"
      },
      "phone_number": "+1234567890"
    }
  ]
}
```

#### GET /jobapply/my_applications/{app_id}
Get details of a specific application (Admin only).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "application": {
    "id": "uuid",
    "job_id": "job-uuid",
    "applicant_name": "Applicant Name",
    "user_email": "user@example.com",
    "status": "Applied",
    "created_at": "2023-01-01T00:00:00Z",
    "jobs": {
      "title": "Job Title"
    }
  }
}
```

#### PATCH /jobapply/applications/{app_id}/status
Update application status (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "approved"
}
```

**Response (200):**
```json
{
  "message": "Application status updated successfully"
}
```

#### DELETE /jobapply/applications/{app_id}
Withdraw an application.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200):**
```json
{
  "message": "Application withdrawn successfully"
}
```

### Email Notification Endpoints

#### PATCH /emails/applications/{app_id}/status
Update application status and send email notification (Admin/Subadmin only).

**Headers:**
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "status": "approved"
}
```

**Response (200):**
```json
{
  "message": "status updated and email sent"
}
```

## 🔐 Authentication & Authorization

### Token-Based Authentication
The API uses JWT tokens for authentication. After successful login, clients receive an access token that must be included in the `Authorization` header for protected endpoints.

### Role-Based Access Control
The system implements three user roles:

- **Admin**: Full access to all operations
- **Subadmin**: Access to admin-level operations (same as admin in current implementation)
- **User**: Limited access (cannot create/update/delete content)

**Role Assignment:**
- User roles are stored in the `user_roles` table in Supabase
- After user signup, roles must be manually assigned by an admin
- Role is checked on every protected endpoint using `check_admin_or_subadmin()` function

### Protected Endpoints
The following endpoints require admin or subadmin privileges:
- Blog management (create, update, delete)
- Job management (create, update, delete, close)
- Application status updates with email notifications

**Role Checking Logic:**
- `get_current_user()`: Verifies JWT token and returns user object
- `check_admin_or_subadmin()`: Checks if user has 'admin' or 'subadmin' role
- Returns 403 Forbidden if user has no role or role is not admin/subadmin

## 🗄️ Database Schema

### Required Supabase Tables

#### user_roles
Stores user role assignments.
```sql
CREATE TABLE user_roles (
  user_id UUID REFERENCES auth.users(id) PRIMARY KEY,
  role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'subadmin', 'user')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### blogs
Stores blog post information.
```sql
CREATE TABLE blogs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  thumbnail TEXT,
  internal_urls TEXT[],
  created_by UUID REFERENCES auth.users(id),
  author VARCHAR(100) NOT NULL,
  tags TEXT[],
  category VARCHAR(100) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### jobs
Stores job posting information.
```sql
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title VARCHAR(255) NOT NULL,
  department VARCHAR(100) NOT NULL,
  employment_type VARCHAR(50) NOT NULL,
  job_description TEXT,
  qualifications TEXT NOT NULL,
  salary_range VARCHAR(100),
  location VARCHAR(255),
  status VARCHAR(20) DEFAULT 'live' CHECK (status IN ('live', 'closed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### applications
Stores job application information.
```sql
CREATE TABLE applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID REFERENCES jobs(id),
  title VARCHAR(255),  -- Job title (retrieved from job_id)
  user_email VARCHAR(255) NOT NULL,
  applicant_name VARCHAR(255) NOT NULL,
  resume_url TEXT,
  phone_number VARCHAR(20),
  status VARCHAR(50) DEFAULT 'Applied',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### email_templates
Stores email templates for different statuses.
```sql
CREATE TABLE email_templates (
  status VARCHAR(50) PRIMARY KEY,
  subject VARCHAR(255) NOT NULL,
  body TEXT NOT NULL
);
```

### Supabase Storage Buckets

#### resumes
Stores uploaded resume files.
- **Bucket Name**: `resumes`
- **File Format**: PDF
- **Access**: Public (for download links)

## 🖼️ Image Upload Configuration

### Cloudinary Setup
Images are uploaded to Cloudinary for efficient storage and delivery.

### Supported Image Operations
- **Thumbnail Upload**: Single image for blog posts
- **Internal Images**: Multiple images within blog content
- **Automatic Optimization**: Cloudinary handles image optimization
- **Secure URLs**: HTTPS delivery with CDN support

### File Upload Best Practices
1. Use `multipart/form-data` for file uploads
2. Set appropriate file size limits on the client
3. Validate file types before upload
4. Handle upload errors gracefully

## 📧 Email Configuration

### SMTP Setup
The email system uses Gmail's SMTP server for sending notifications.

### Required Email Templates
Create entries in the `email_templates` table for each application status:

```sql
INSERT INTO email_templates (status, subject, body) VALUES
('approved', 'Application Approved', 'Congratulations! Your application has been approved.'),
('rejected', 'Application Rejected', 'We regret to inform you that your application has been rejected.'),
('pending', 'Application Received', 'Thank you for your application. We will review it shortly.'),
('under_review', 'Application Under Review', 'Your application is currently under review.');
```

### Email Security
- Use app-specific passwords for Gmail
- Never commit email credentials to version control
- Consider using environment-specific email accounts

## 💡 Usage Examples

### Python Client Example
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# 1. User Registration
signup_data = {
    "email": "user@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/signup", json=signup_data)
print(response.json())

# 2. User Login
login_data = {
    "email": "user@example.com",
    "password": "password123"
}
response = requests.post(f"{BASE_URL}/login", json=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Create Blog Post
blog_data = {
    "title": "My First Blog Post",
    "content": "This is the content of my blog post...",
    "author": "John Doe",
    "tags": "python,fastapi,web",
    "category": "Technology"
}
files = {
    "image": open("thumbnail.jpg", "rb")
}
response = requests.post(f"{BASE_URL}/blogs/", headers=headers, data=blog_data, files=files)
print(response.json())
```

### JavaScript/Fetch Example
```javascript
const BASE_URL = "http://localhost:8000";

// 1. Login
async function login(email, password) {
    const response = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    return data.access_token;
}

// 2. Create Blog Post
async function createBlog(token, blogData, imageFile) {
    const formData = new FormData();
    formData.append("title", blogData.title);
    formData.append("content", blogData.content);
    formData.append("author", blogData.author);
    formData.append("tags", blogData.tags);
    formData.append("category", blogData.category);
    if (imageFile) {
        formData.append("image", imageFile);
    }

    const response = await fetch(`${BASE_URL}/blogs/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`
        },
        body: formData
    });
    return response.json();
}
```

## ⚠️ Error Handling

### Error Response Format
All error responses follow this standard format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes
- **400 Bad Request**: Invalid input, file upload failed, database errors, missing required fields
- **401 Unauthorized**: Missing or invalid authentication token, expired token
- **403 Forbidden**: User role does not permit this action, insufficient permissions
- **404 Not Found**: Requested resource does not exist, job not found, application not found
- **500 Internal Server Error**: Unexpected server error, database connection issues, SMTP errors

### Error Handling Patterns in Code
The application uses a layered error handling approach:

1. **Specific Error Handling**: Each endpoint catches specific exceptions and returns appropriate HTTP status codes
2. **HTTPException Re-raising**: When an HTTPException is caught, it's re-raised to preserve the status code
3. **Global Exception Handler**: A global handler catches any unhandled exceptions and returns 500 errors with CORS headers

**Example Error Handling Pattern:**
```python
try:
    # Operation that might fail
    check_admin_or_subadmin(user)  # May raise 403
    # ... other operations ...
except HTTPException:
    raise  # Preserve status code
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
```

### Common Error Scenarios

#### Authentication Errors
- **401**: Invalid token, expired token, missing Authorization header
- **403**: User role not found, user is not admin/subadmin

#### File Upload Errors
- **400**: No file provided, Cloudinary upload failed, invalid file type
- **500**: Cloudinary service unavailable, network issues

#### Database Errors
- **400**: Database insert/update failed, constraint violations
- **404**: Record not found (job, blog, application)
- **500**: Database connection issues, service unavailable

#### Email Errors
- **500**: SMTP connection failed, invalid credentials, email service unavailable

### Error Handling Best Practices
1. Always check response status codes before processing response data
2. Handle specific error cases appropriately (e.g., show user-friendly messages for 403 errors)
3. Provide user-friendly error messages that don't expose sensitive information
4. Log errors on the server side for debugging purposes
5. Implement retry logic for transient failures (network issues, temporary service unavailability)
6. Use appropriate error messages for different user roles (admin vs regular user)

## 🌐 CORS Configuration

### Default Origins
The application is configured to allow requests from:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://localhost:3000`
- `https://admin-section-mehdi-tech.vercel.app`

### Adding New Origins
To add a new frontend origin:

1. Edit the `origins` list in `main.py`
2. Add the exact URL (no trailing slash)
3. Restart the server

```python
origins = [
    "http://localhost:5173",
    "https://your-frontend-domain.com"  # Add your domain here
]
```

### CORS Requirements
- Include `Origin` header in requests (browser does this automatically)
- For file uploads: use `multipart/form-data` content type
- For protected endpoints: include `Authorization: Bearer {token}` header

## 🛠️ Development

### Development Server
```bash
uvicorn main:app --reload
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code documentation
- Implement proper error handling
- Use async/await for I/O operations

### Testing
Consider using:
- **pytest** for unit testing
- **httpx** for API testing
- **factory-boy** for test data generation

## 🚀 Deployment

### Production Server
```bash
# Using Gunicorn (recommended for production)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or using Uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Environment Variables in Production
Set all required environment variables in your production environment:
- Use secure, production-specific credentials
- Enable HTTPS in production
- Configure proper CORS origins
- Set appropriate logging levels

### Docker Deployment
Consider containerizing the application for easier deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Support

For support and questions:

1. **Check the API documentation**: http://localhost:8000/docs
2. **Review error messages**: Check server logs for detailed error information
3. **Verify configuration**: Ensure all environment variables are set correctly
4. **Test with simple requests**: Use curl or Postman to test endpoints
5. **Check Supabase dashboard**: Verify tables and data exist
6. **Review Cloudinary dashboard**: Check image uploads and credentials

### Common Issues

#### CORS Errors
- Verify frontend origin is in the allowed origins list
- Check that the server has been restarted after adding origins
- Ensure the frontend is sending the correct Origin header

#### Authentication Failures
- Verify the JWT token is being sent in the Authorization header
- Check that the token hasn't expired
- Ensure the user has the correct role for the requested operation

#### File Upload Issues
- Verify file size limits are appropriate
- Check that the correct content type is being used
- Ensure Cloudinary credentials are correct

#### Database Connection Issues
- Verify Supabase URL and service role key are correct
- Check that the required tables exist in Supabase
- Ensure the database is accessible from your environment

---

**Note**: This API is designed for integration with frontend applications. Always use HTTPS in production and follow security best practices when handling user data and authentication tokens.