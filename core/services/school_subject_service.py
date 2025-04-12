from typing import TYPE_CHECKING, List, Union

from fastapi import HTTPException

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

    async def create_subject_v2(
        self, create_data: Union[SchoolSubjectCreate, List[SchoolSubjectCreate]]
    ) -> Union[SchoolSubject, List[SchoolSubject]]:
        """
        Создает один или несколько учебных предметов в указанной школе.

        Поддерживает как создание одиночного предмета, так и массовое создание.
        Все предметы должны принадлежать одной школе.

        Args:
            create_data: Данные для создания предмета/предметов. Может быть:
                - Single SchoolSubjectCreate для создания одного предмета
                - List[SchoolSubjectCreate] для массового создания

        Returns:
            Созданные предметы в том же формате, что и входные данные:
            - SchoolSubject для одиночного создания
            - List[SchoolSubject] для массового создания

        Raises:
            HTTPException: 404 если указанная школа не найдена
            HTTPException: 400 если возникает конфликт уникальности (предмет уже существует)
            HTTPException: 422 если:
                - Переданы предметы для разных школ
                - Невалидные данные в запросе

        """
        is_one = isinstance(create_data, SchoolSubjectCreate)
        create_data = (
            [create_data]
            if isinstance(create_data, SchoolSubjectCreate)
            else create_data
        )

        school_ids = {create_data.school_id for create_data in create_data}

        if len(school_ids) > 1:
            raise HTTPException(
                status_code=422,
                detail=[
                    {
                        "loc": ["body"],
                        "msg": "Schools must be the same",
                        "type": "value_error",
                    }
                ],
            )

        await self.get_school(school_ids.pop())  # for validate school in bd

        subject_repo: SchoolSubjectRepository = self.get_repo("school_subject")
        subjects = await subject_repo.multiple_create(create_data)

        return subjects[0] if is_one else subjects

    async def create_subject(self, create_data: SchoolSubjectCreate) -> SchoolSubject:
        await self.get_school(create_data.school_id)  # for validate school in bd
        repo = self.get_repo("school_subject")
        return await repo.create(create_data)

    async def get_school(self, school_id: int) -> School:
        repo = self.get_repo("school")
        return await repo.get_by_id(item_id=school_id, error_message="School not found")

    async def get_subjects(self, school_id: int) -> List[SchoolSubjectRead]:
        school = await self.get_school(school_id)
        return school.school_subject
