"""
Monetization API Routes
Handle affiliate campaigns and revenue tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db, AffiliateCampaign

router = APIRouter()

# Schemas
class CampaignRequest(BaseModel):
    name: str
    product_type: str
    affiliate_link: str
    commission_rate: float

class CampaignResponse(BaseModel):
    id: int
    name: str
    product_type: str
    affiliate_link: str
    commission_rate: float
    clicks: int
    conversions: int
    revenue: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/campaigns", response_model=List[CampaignResponse])
async def get_all_campaigns(db: Session = Depends(get_db)):
    """Get all affiliate campaigns"""
    campaigns = db.query(AffiliateCampaign).all()
    return campaigns

@router.get("/campaigns/active", response_model=List[CampaignResponse])
async def get_active_campaigns(db: Session = Depends(get_db)):
    """Get active campaigns"""
    campaigns = db.query(AffiliateCampaign).filter(
        AffiliateCampaign.is_active == True
    ).all()
    return campaigns

@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(campaign: CampaignRequest, db: Session = Depends(get_db)):
    """Create new affiliate campaign"""

    new_campaign = AffiliateCampaign(
        name=campaign.name,
        product_type=campaign.product_type,
        affiliate_link=campaign.affiliate_link,
        commission_rate=campaign.commission_rate
    )

    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)

    return new_campaign

@router.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: int,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    """Update campaign status"""

    campaign = db.query(AffiliateCampaign).filter(
        AffiliateCampaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if is_active is not None:
        campaign.is_active = is_active

    db.commit()
    db.refresh(campaign)

    return campaign

@router.post("/campaigns/{campaign_id}/click")
async def track_click(campaign_id: int, db: Session = Depends(get_db)):
    """Track affiliate link click"""

    campaign = db.query(AffiliateCampaign).filter(
        AffiliateCampaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.clicks += 1
    db.commit()

    return {"success": True, "clicks": campaign.clicks}

@router.post("/campaigns/{campaign_id}/conversion")
async def track_conversion(
    campaign_id: int,
    amount: float,
    db: Session = Depends(get_db)
):
    """Track affiliate conversion"""

    campaign = db.query(AffiliateCampaign).filter(
        AffiliateCampaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.conversions += 1
    campaign.revenue += amount * (campaign.commission_rate / 100)

    db.commit()

    return {
        "success": True,
        "conversions": campaign.conversions,
        "revenue": campaign.revenue
    }

@router.get("/revenue/summary")
async def get_revenue_summary(db: Session = Depends(get_db)):
    """Get revenue summary"""

    from sqlalchemy import func

    total_revenue = db.query(func.sum(AffiliateCampaign.revenue)).scalar() or 0
    total_clicks = db.query(func.sum(AffiliateCampaign.clicks)).scalar() or 0
    total_conversions = db.query(func.sum(AffiliateCampaign.conversions)).scalar() or 0

    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

    return {
        "total_revenue": total_revenue,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "conversion_rate": conversion_rate
    }

@router.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Delete campaign"""

    campaign = db.query(AffiliateCampaign).filter(
        AffiliateCampaign.id == campaign_id
    ).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()

    return {"success": True, "message": "Campaign deleted"}
