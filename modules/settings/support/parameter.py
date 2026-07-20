# parameter.py
from typing import Optional
from sqlalchemy import (
    Integer,
    String
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import Base

class Parameter(Base):
    __tablename__ = "ta_parametro"

    id_parametro: Mapped[int] = mapped_column(
        "ID_PARAMETRO",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nm_parametro: Mapped[str] = mapped_column(
        "NM_PARAMETRO",
        String(100),
        nullable=False,
        unique=True
    )

    ds_parametro: Mapped[str] = mapped_column(
        "DS_PARAMETRO",
        String(500),
        nullable=False
    )

    nm_tabela: Mapped[Optional[str]] = mapped_column(
        "NM_TABELA",
        String(100),
        nullable=True
    )

    nm_campo: Mapped[Optional[str]] = mapped_column(
        "NM_CAMPO",
        String(100),
        nullable=True
    )
