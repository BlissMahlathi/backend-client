import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import supabase

load_dotenv()

app = FastAPI(title="Admin API Backend")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables")

supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================================
# Authentication Middleware
# ============================================================================
async def verify_auth_token(authorization: Optional[str] = Header(default=None)):
    """Verify JWT token from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    
    token = authorization.replace("Bearer ", "")
    try:
        user = supabase_client.auth.get_user(token)
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# ============================================================================
# Pydantic Models
# ============================================================================
class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None
    published_at: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published_at: Optional[str] = None


class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    instructor: Optional[str] = None


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None


class DealCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class DealUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class GalleryCreate(BaseModel):
    title: str
    image_url: str
    alt_text: Optional[str] = None


class GalleryUpdate(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    alt_text: Optional[str] = None


# ============================================================================
# Blog Posts Endpoints
# ============================================================================
@app.get("/api/admin/blogs")
async def get_blogs(authorization: Optional[str] = Header(default=None)):
    """Fetch all blog posts"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("posts").select("*").order("published_at", desc=True).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/blogs")
async def create_blog(post: PostCreate, authorization: Optional[str] = Header(default=None)):
    """Create a new blog post"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("posts").insert(post.model_dump()).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/blogs/{post_id}")
async def update_blog(post_id: str, post: PostUpdate, authorization: Optional[str] = Header(default=None)):
    """Update a blog post"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("posts").update(post.model_dump(exclude_unset=True)).eq("id", post_id).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/admin/blogs/{post_id}")
async def delete_blog(post_id: str, authorization: Optional[str] = Header(default=None)):
    """Delete a blog post"""
    try:
        await verify_auth_token(authorization)
        supabase_client.table("posts").delete().eq("id", post_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Courses Endpoints
# ============================================================================
@app.get("/api/admin/courses")
async def get_courses(authorization: Optional[str] = Header(default=None)):
    """Fetch all courses"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("courses").select("*").order("created_at", desc=True).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/courses")
async def create_course(course: CourseCreate, authorization: Optional[str] = Header(default=None)):
    """Create a new course"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("courses").insert(course.model_dump()).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/courses/{course_id}")
async def update_course(course_id: str, course: CourseUpdate, authorization: Optional[str] = Header(default=None)):
    """Update a course"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("courses").update(course.model_dump(exclude_unset=True)).eq("id", course_id).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/admin/courses/{course_id}")
async def delete_course(course_id: str, authorization: Optional[str] = Header(default=None)):
    """Delete a course"""
    try:
        await verify_auth_token(authorization)
        supabase_client.table("courses").delete().eq("id", course_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Deals Endpoints
# ============================================================================
@app.get("/api/admin/deals")
async def get_deals(authorization: Optional[str] = Header(default=None)):
    """Fetch all deals"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("deals").select("*").order("created_at", desc=True).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/deals")
async def create_deal(deal: DealCreate, authorization: Optional[str] = Header(default=None)):
    """Create a new deal"""
    try:
        await verify_auth_token(authorization)
        
        # Server-side validation
        if deal.price is not None:
            try:
                float(deal.price)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Price must be a number")
        
        if deal.start_date:
            try:
                datetime.fromisoformat(deal.start_date)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid start_date")
        
        if deal.end_date:
            try:
                datetime.fromisoformat(deal.end_date)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid end_date")
        
        if deal.start_date and deal.end_date:
            start = datetime.fromisoformat(deal.start_date)
            end = datetime.fromisoformat(deal.end_date)
            if start > end:
                raise HTTPException(status_code=400, detail="start_date must be before end_date")
        
        data = supabase_client.table("deals").insert(deal.model_dump()).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/deals/{deal_id}")
async def update_deal(deal_id: str, deal: DealUpdate, authorization: Optional[str] = Header(default=None)):
    """Update a deal"""
    try:
        await verify_auth_token(authorization)
        
        # Server-side validation
        if deal.price is not None:
            try:
                float(deal.price)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Price must be a number")
        
        if deal.start_date:
            try:
                datetime.fromisoformat(deal.start_date)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid start_date")
        
        if deal.end_date:
            try:
                datetime.fromisoformat(deal.end_date)
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="Invalid end_date")
        
        if deal.start_date and deal.end_date:
            start = datetime.fromisoformat(deal.start_date)
            end = datetime.fromisoformat(deal.end_date)
            if start > end:
                raise HTTPException(status_code=400, detail="start_date must be before end_date")
        
        data = supabase_client.table("deals").update(deal.model_dump(exclude_unset=True)).eq("id", deal_id).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/admin/deals/{deal_id}")
async def delete_deal(deal_id: str, authorization: Optional[str] = Header(default=None)):
    """Delete a deal"""
    try:
        await verify_auth_token(authorization)
        supabase_client.table("deals").delete().eq("id", deal_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Gallery Endpoints
# ============================================================================
@app.get("/api/admin/galleries")
async def get_galleries(authorization: Optional[str] = Header(default=None)):
    """Fetch all gallery items"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("galleries").select("*").order("created_at", desc=True).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/admin/galleries")
async def create_gallery(gallery: GalleryCreate, authorization: Optional[str] = Header(default=None)):
    """Create a new gallery item"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("galleries").insert(gallery.model_dump()).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/admin/galleries/{gallery_id}")
async def update_gallery(gallery_id: str, gallery: GalleryUpdate, authorization: Optional[str] = Header(default=None)):
    """Update a gallery item"""
    try:
        await verify_auth_token(authorization)
        data = supabase_client.table("galleries").update(gallery.model_dump(exclude_unset=True)).eq("id", gallery_id).execute()
        return data.data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/admin/galleries/{gallery_id}")
async def delete_gallery(gallery_id: str, authorization: Optional[str] = Header(default=None)):
    """Delete a gallery item"""
    try:
        await verify_auth_token(authorization)
        supabase_client.table("galleries").delete().eq("id", gallery_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Health Check
# ============================================================================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
