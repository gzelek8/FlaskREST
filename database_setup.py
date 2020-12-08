from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UnityError(Base):
    __tablename__ = 'unity_error'

    id = Column(Integer, primary_key=True)
    line = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250))

    @property
    def serialize(self):
        return {
            'line': self.line,
            'name': self.name,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///unity-errors.db')
Base.metadata.create_all(engine)
