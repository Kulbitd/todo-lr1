"""Todo models
"""
from enum import Enum
from sqlalchemy import Column, Integer, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    """Todo model
    """
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    title = Column(Text)
    completed = Column(Boolean, default=False)
    tag = Column(Text, default="plans")

class Tags(str, Enum):
    studies = "studies"
    personal = "personal"
    plans = "plans"

    def __repr__(self):
        return f'<Todo {self.id}>'
