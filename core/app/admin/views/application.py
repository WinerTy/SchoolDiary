from starlette_admin.contrib.sqla import ModelView

from starlette_admin import action
from fastapi import Request
from typing import List, Any

from core.database.utils import db_helper
from core.database import Applications

class ApplicationAdmin(ModelView):

    label = "Заявки"
    name = "Заявка"

    column_visibility = [
        "id",
        "director_full_name",
        "director_phone",
        "director_email",
        "created_at",
        "status",
    ]

    fields = column_visibility

    @action(
        name="debug_application",
        text="Обработать заявки",
        confirmation="Заявки будут обработаны автоматически, отменить данное действие нельзя!",
        submit_btn_text="Обработать",
        submit_btn_class="btn-success",
    )
    async def debug_application_action(self, request: Request, pks: List[Any]):
        
        async with db_helper.session_factory() as session:
            for id in pks:
                res = await session.get(Applications, int(id))
                print(res.to_dict)
        return f"Завершено"