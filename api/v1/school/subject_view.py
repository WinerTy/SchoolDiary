from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.services.get_service import get_school_subject_service
from core.database.crud.school_subject import (
    SchoolSubjectCreate,
    SchoolSubjectCreateRequest,
    SchoolSubjectRead,
)
from core.services.school_subject_service import SchoolSubjectService

router: APIRouter = APIRouter(
    prefix="/subject",
    tags=["School"],
)


@router.post("/{school_id}", response_model=SchoolSubjectRead)
async def create_subject_for_school(
    school_id: int,
    subject_data: SchoolSubjectCreateRequest,
    service: Annotated["SchoolSubjectService", Depends(get_school_subject_service)],
):
    result = await service.create_subject(
        SchoolSubjectCreate(school_id=school_id, subject_name=subject_data.subject_name)
    )
    return result


@router.get("/{school_id}")
async def get_school_subjects(
    school_id: int,
    service: Annotated["SchoolSubjectService", Depends(get_school_subject_service)],
):
    result = await service.get_subjects(school_id)
    return result
