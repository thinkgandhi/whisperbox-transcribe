import uuid
from typing import Optional

from sqlalchemy import JSON, VARCHAR, Column, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Mapped, declarative_mixin  # type: ignore

from .schemas import ArtifactType, JobStatus, JobType

Base = declarative_base()


@declarative_mixin
class WithStandardFields:
    """Mixin that adds standard fields (id, created_at, updated_at)."""

    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return Column(DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls) -> Mapped[Optional[DateTime]]:
        return Column(DateTime, onupdate=func.now())

    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return Column(
            VARCHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
        )


class Job(Base, WithStandardFields):
    __tablename__ = "jobs"

    url = Column(String(length=2048))
    status = Column(Enum(JobStatus), nullable=False)
    config = Column(JSON(none_as_null=True))
    meta = Column(JSON(none_as_null=True))
    type = Column(Enum(JobType), nullable=False)


class Artifact(Base, WithStandardFields):
    __tablename__ = "artifacts"

    job_id = Column(
        VARCHAR(36),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
    )

    data = Column(JSON(none_as_null=True))
    type = Column(Enum(ArtifactType), nullable=False)
