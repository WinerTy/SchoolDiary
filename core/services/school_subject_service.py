from typing import TYPE_CHECKING, List

from core.database import SchoolSubject, School
from core.database.crud.school_subject import (
    SchoolSubjectCreate,
    SchoolSubjectUpdate,
    SchoolSubjectRead,
)
from core.services.base_services import BaseService

if TYPE_CHECKING:
    from core.database.crud.school_subject import SchoolSubjectRepository
    from core.database.crud import SchoolRepository


class SchoolSubjectService(
    BaseService[
        SchoolSubject, SchoolSubjectCreate, SchoolSubjectUpdate, SchoolSubjectRead
    ]
):
    def __init__(
        self,
        school_subject_repo: "SchoolSubjectRepository",
        school_repo: "SchoolRepository",
    ):
        super().__init__(
            repositories={"school_subject": school_subject_repo, "school": school_repo},
        )

    async def create_subject(self, create_data: SchoolSubjectCreate) -> SchoolSubject:
        await self.get_school(create_data.school_id)  # for validate school in bd
        repo = self.get_repo("school_subject")
        return await repo.create(create_data)

    async def get_school(self, school_id: int) -> School:
        repo = self.get_repo("school")
        return await repo.get_by_id(school_id)

    async def get_subjects(self, school_id: int) -> List[SchoolSubjectRead]:
        school = await self.get_school(school_id)
        return school.school_subject
