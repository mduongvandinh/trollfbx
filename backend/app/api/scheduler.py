"""
Scheduler API Routes
Control automated posting schedule
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.scheduler_service import scheduler_service

router = APIRouter()

class SchedulerStatus(BaseModel):
    is_running: bool
    jobs: list

@router.get("/status", response_model=SchedulerStatus)
async def get_scheduler_status():
    """Get scheduler status"""
    jobs = []

    if scheduler_service.is_running:
        for job in scheduler_service.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": str(job.next_run_time) if job.next_run_time else None
            })

    return {
        "is_running": scheduler_service.is_running,
        "jobs": jobs
    }

@router.post("/start")
async def start_scheduler():
    """Start the scheduler"""
    scheduler_service.start()
    return {"success": True, "message": "Scheduler started"}

@router.post("/stop")
async def stop_scheduler():
    """Stop the scheduler"""
    scheduler_service.stop()
    return {"success": True, "message": "Scheduler stopped"}

@router.post("/trigger/news")
async def trigger_news_fetch():
    """Manually trigger news fetching"""
    scheduler_service.fetch_news_job()
    return {"success": True, "message": "News fetch triggered"}

@router.post("/trigger/post")
async def trigger_auto_post():
    """Manually trigger auto-posting"""
    scheduler_service.auto_post_job()
    return {"success": True, "message": "Auto-post triggered"}

@router.post("/trigger/analytics")
async def trigger_analytics_fetch():
    """Manually trigger analytics fetching"""
    scheduler_service.fetch_analytics_job()
    return {"success": True, "message": "Analytics fetch triggered"}

@router.post("/trigger/daily-plan")
async def trigger_daily_plan():
    """Manually trigger daily content planning"""
    scheduler_service.generate_daily_plan()
    return {"success": True, "message": "Daily plan generated"}
