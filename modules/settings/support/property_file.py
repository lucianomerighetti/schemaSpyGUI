# property_file.py
from sqlalchemy import (
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import Base

class PropertyFile(Base):
    __tablename__ = "tb_arquivo_propriedade"

    id_arquivo_propriedade: Mapped[int] = mapped_column(
        "ID_ARQUIVO_PROPRIEDADE",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_configuracao: Mapped[int] = mapped_column(
        "ID_CONFIGURACAO",
        Integer,
        ForeignKey("tb_configuracao.ID_CONFIGURACAO", ondelete="CASCADE"),
        nullable=False
    )

    nm_chave: Mapped[str] = mapped_column(
        "NM_CHAVE",
        String(100),
        nullable=False
    )

    vl_valor: Mapped[str] = mapped_column(
        "VL_VALOR",
        String(500),
        nullable=False
    )
