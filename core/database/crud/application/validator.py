
from core.database.crud.base import BaseValidator


from typing import TYPE_CHECKING

from fastapi.exceptions import HTTPException
from core.database.models.choices import ChoicesApplicationStatus
from core.database import Applications

class ApplicationValidator(BaseValidator):
    def validate_permisions(self, instance: Applications, user_id: int):
        if instance.status != ChoicesApplicationStatus.pending:
            raise HTTPException(detail=f"Application Status different from {ChoicesApplicationStatus.pending.value}", status_code=400) 
        
        if instance.user_id != user_id:
            raise HTTPException(detail="You don't have permisions to change this application")
        