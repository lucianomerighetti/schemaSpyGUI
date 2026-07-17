# Artefato:  project.py

from typing import Optional
from sqlalchemy import (
    Integer,
    String
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import (
    Base
)

class Project(Base):

    __tablename__ = "tb_projeto"

    id_projeto: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nm_projeto: Mapped[str] = mapped_column(
        String(100)
    )

    tp_database: Mapped[str] = mapped_column(
        String(50)
    )

    nm_host: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    nm_schema: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )
    
    nu_porta: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )