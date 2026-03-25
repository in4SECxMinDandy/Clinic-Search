"""
Review Service - Reviews Router
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from review_service.models.models import Review, ReviewReport
from review_service.schemas.schemas import ReviewCreate, ReviewReply, ReviewReport as ReviewReportSchema, ReviewResponse
from review_service.utils.dependencies import get_db, get_current_user
from datetime import datetime

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_review(
    request: ReviewCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a review for a completed booking"""
    # Check if booking exists and is completed
    # In real implementation, verify booking belongs to user and is completed

    review = Review(
        booking_id=request.booking_id,
        user_id=current_user["user_id"],
        clinic_id="",  # Would come from booking
        doctor_id="",  # Would come from booking
        rating=request.rating,
        comment=request.comment,
        pros=request.pros,
        cons=request.cons,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return ReviewResponse(
        id=str(review.id),
        booking_id=str(review.booking_id),
        user_id=str(review.user_id),
        clinic_id=str(review.clinic_id),
        doctor_id=str(review.doctor_id),
        rating=review.rating,
        comment=review.comment,
        pros=review.pros,
        cons=review.cons,
        is_hidden=review.is_hidden,
        is_reported=review.is_reported,
        report_count=review.report_count or 0,
        created_at=review.created_at,
        updated_at=review.updated_at,
    )


@router.get("/clinic/{clinic_id}")
async def get_clinic_reviews(
    clinic_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get reviews for a clinic"""
    result = await db.execute(
        select(Review)
        .where(Review.clinic_id == clinic_id)
        .where(Review.is_hidden == False)
        .order_by(Review.created_at.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    reviews = result.scalars().all()

    return {
        "reviews": [
            ReviewResponse(
                id=str(r.id),
                booking_id=str(r.booking_id),
                user_id=str(r.user_id),
                clinic_id=str(r.clinic_id),
                doctor_id=str(r.doctor_id),
                rating=r.rating,
                comment=r.comment,
                pros=r.pros,
                cons=r.cons,
                is_hidden=r.is_hidden,
                reply=r.reply,
                replied_at=r.replied_at,
                is_reported=r.is_reported,
                report_count=r.report_count or 0,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ],
        "page": page,
        "page_size": page_size,
    }


@router.get("/doctor/{doctor_id}")
async def get_doctor_reviews(
    doctor_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get reviews for a doctor"""
    result = await db.execute(
        select(Review)
        .where(Review.doctor_id == doctor_id)
        .where(Review.is_hidden == False)
        .order_by(Review.created_at.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    reviews = result.scalars().all()

    return {
        "reviews": [
            ReviewResponse(
                id=str(r.id),
                booking_id=str(r.booking_id),
                user_id=str(r.user_id),
                clinic_id=str(r.clinic_id),
                doctor_id=str(r.doctor_id),
                rating=r.rating,
                comment=r.comment,
                pros=r.pros,
                cons=r.cons,
                is_hidden=r.is_hidden,
                reply=r.reply,
                replied_at=r.replied_at,
                is_reported=r.is_reported,
                report_count=r.report_count or 0,
                created_at=r.created_at,
                updated_at=r.updated_at,
            )
            for r in reviews
        ],
        "page": page,
        "page_size": page_size,
    }


@router.post("/{review_id}/reply")
async def reply_review(
    review_id: str,
    request: ReviewReply,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reply to a review (clinic owner or doctor)"""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.reply:
        raise HTTPException(status_code=400, detail="Already replied")

    review.reply = request.reply
    review.replied_by = current_user["user_id"]
    review.replied_at = datetime.utcnow()

    await db.commit()
    await db.refresh(review)

    return {"message": "Reply added"}


@router.post("/{review_id}/report")
async def report_review(
    review_id: str,
    request: ReviewReportSchema,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Report a review"""
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Create report
    report = ReviewReport(
        review_id=review.id,
        reporter_id=current_user["user_id"],
        reason=request.reason,
        description=request.description,
    )
    db.add(report)

    # Update review
    review.report_count = (review.report_count or 0) + 1
    if review.report_count >= 3:
        review.is_reported = True

    await db.commit()

    return {"message": "Report submitted"}
