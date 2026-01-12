# FastAPI Blog Management API Documentation

This is a FastAPI application for user authentication and blog management using Supabase for database and authentication, and Cloudinary for image uploads.

## Setup

1. Install dependencies:
   ```
   pip install fastapi uvicorn supabase python-dotenv cloudinary
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
- 200: `{"access_token": "string", "token_type": "bearer"}`
- 401: `{"detail": "invalid credentials"}`

#### GET /admin
Access the admin dashboard (requires admin role).

**Headers:**
- Authorization: Bearer <token>

**Response:**
- 200: `{"message": "Welcome to the admin dashboard"}`
- 401: `{"detail": "invalid token"}`
- 403: `{"detail": "Role not found"}` or `{"detail": "Access forbidden: Admins only"}`

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
  "images_url": "string"
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

## Database Schema

### user_roles table
- user_id: string
- role: string (admin, subadmin, etc.)

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

## Notes

- Image uploads are handled via Cloudinary.
- Roles are checked against the `user_roles` table in Supabase.
- All blog operations require admin or subadmin privileges.
- The application uses Supabase for authentication and database operations.