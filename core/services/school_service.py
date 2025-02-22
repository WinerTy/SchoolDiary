from core.database import School
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool
from .base_services import BaseService


class SchoolService(BaseService[School, CreateSchool, ReadSchool, ReadSchool]):
    def __init__(
        self,
        school_repo: BaseRepository,
        subject_repo: BaseRepository,
        lesson_repo: BaseRepository,
    ):
        super().__init__(
            repositories={
                "school": school_repo,
                "subject": subject_repo,
                "lesson": lesson_repo,
            }
        )
