# project.py

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

    nm_host: Mapped[str] = mapped_column(
        String(255)
    )

    nm_schema: Mapped[str] = mapped_column(
        String(100)
    )
    
    nu_porta: Mapped[int] = mapped_column(
        Integer
    )