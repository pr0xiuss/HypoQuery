from pydantic import BaseModel


class ConstraintResponse(BaseModel):
    name: str

    constraint_type: str

    definition: str