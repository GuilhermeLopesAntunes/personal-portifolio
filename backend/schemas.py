from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title: str
    description: str
    stack_ids: list[int] = [] 


class StackCreate(BaseModel):
    name: str
    svg_icon: str


class StackOut(BaseModel):
    id: int
    name: str
    svg_icon: str

    class Config:
        from_attributes = True

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str
    stacks: list[StackOut] = [] 
    class Config:
        from_attributes = True