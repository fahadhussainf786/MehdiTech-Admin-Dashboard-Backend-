# FastAPI Login, Signup, Blog and Job Management API Documentation

This is a FastAPI application for user authentication, blog management, and job management using Supabase for database and authentication, and Cloudinary for image uploads.

## Setup

1. Install dependencies:
   ```
   pip install fastapi uvicorn supabase python-dotenv cloudinary python-multipart
   ```

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