from os import environ
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Database name
dbname = "project_tracker"

# Get Postgresql URI variable from Conda environment
postgresql_uri = environ.get('POSTGRESQL_URI')

# Create engine
engine = create_engine(postgresql_uri + dbname)

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    title = Column(String(length=60))

    def __repr__(self):
        return f"[Project(project_id={self.project_id}, title={self.title})]"


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    description = Column(String(length=60))

    project = relationship("Project")

    def __repr__(self):
        return f"<<Task(description={self.description})>>"


Base.metadata.create_all(engine)


def create_session():
    session = sessionmaker(bind=engine)
    return session()


if __name__ == "__main__":
    session = create_session()

    clean_house_project = Project(title="Clean House")
    session.add(clean_house_project)
    session.commit()

    task = Task(description="Clean bedroom",
                project_id=clean_house_project.project_id)
    session.add(task)
    session.commit()
