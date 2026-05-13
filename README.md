# Admin API Backend (Python)

This is a separate FastAPI backend that handles all admin CRUD operations for the Next.js static frontend.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with Supabase credentials:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Endpoints

All endpoints require a Bearer token in the `Authorization` header.

### Blogs
- `GET /api/admin/blogs` - Fetch all blog posts
- `POST /api/admin/blogs` - Create new blog post
- `PUT /api/admin/blogs/{post_id}` - Update blog post
- `DELETE /api/admin/blogs/{post_id}` - Delete blog post

### Courses
- `GET /api/admin/courses` - Fetch all courses
- `POST /api/admin/courses` - Create new course
- `PUT /api/admin/courses/{course_id}` - Update course
- `DELETE /api/admin/courses/{course_id}` - Delete course

### Deals
- `GET /api/admin/deals` - Fetch all deals
- `POST /api/admin/deals` - Create new deal
- `PUT /api/admin/deals/{deal_id}` - Update deal
- `DELETE /api/admin/deals/{deal_id}` - Delete deal

### Galleries
- `GET /api/admin/galleries` - Fetch all gallery items
- `POST /api/admin/galleries` - Create new gallery item
- `PUT /api/admin/galleries/{gallery_id}` - Update gallery item
- `DELETE /api/admin/galleries/{gallery_id}` - Delete gallery item

## Architecture

- The Next.js frontend remains a static export (no runtime needed)
- This Python backend provides all dynamic admin functionality
- CORS is enabled for frontend communication
- All endpoints require Supabase JWT authentication
# backend-client
