from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

project_stack = Table(
    "project_stack",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("stack_id", ForeignKey("stacks.id"), primary_key=True),
)

class Projects(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    stacks = relationship("Stack", secondary=project_stack, back_populates="projects")

class Stack(Base):
    __tablename__ = "stacks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    svg_icon = Column(String)
    projects = relationship("Projects", secondary=project_stack, back_populates="stacks")