# setting.py
from typing import Optional
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.database import (
    Base
)

class Setting(Base):
    __tablename__ = "tb_configuracao"

    id_setting: Mapped[int] = mapped_column(
        "ID_CONFIGURACAO",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nm_setting: Mapped[str] = mapped_column(
        "NM_CONFIGURACAO",
        String(100),
        unique=True,
        nullable=False
    )

    id_conexao: Mapped[Optional[int]] = mapped_column(
        "ID_CONEXAO",
        Integer,
        ForeignKey("tb_conexao.ID_CONEXAO", ondelete="CASCADE"),
        nullable=True
    )

    db_driver_path: Mapped[Optional[str]] = mapped_column("DS_DRIVER_PATH", String(1000), nullable=True)
    schemaspy_path: Mapped[Optional[str]] = mapped_column("DS_SCHEMASPY_PATH", String(1000), nullable=True)
    properties_path: Mapped[Optional[str]] = mapped_column("DS_PROPERTIES_PATH", String(1000), nullable=True)
    properties_text: Mapped[Optional[str]] = mapped_column("DS_PROPERTIES_TEXT", String(1000), nullable=True)
    high_quality: Mapped[bool] = mapped_column("FL_HIGH_QUALITY", Boolean, default=False)
    low_quality: Mapped[bool] = mapped_column("FL_LOW_QUALITY", Boolean, default=False)
    single_sign_on: Mapped[bool] = mapped_column("FL_SINGLE_SIGN_ON", Boolean, default=False)
    show_finish: Mapped[bool] = mapped_column("FL_SHOW_FINISH", Boolean, default=False)
    a_html: Mapped[bool] = mapped_column("FL_A_HTML", Boolean, default=False)
    no_html: Mapped[bool] = mapped_column("FL_NO_HTML", Boolean, default=False)
    dinc_fk: Mapped[bool] = mapped_column("FL_DINC_FK", Boolean, default=False)
    no_ads: Mapped[bool] = mapped_column("FL_NO_ADS", Boolean, default=False)
    no_logo: Mapped[bool] = mapped_column("FL_NO_LOGO", Boolean, default=False)
    no_rows: Mapped[bool] = mapped_column("FL_NO_ROWS", Boolean, default=False)
    rails: Mapped[bool] = mapped_column("FL_RAILS", Boolean, default=False)

    # Tab 3: Output Options Form
    output_dir: Mapped[Optional[str]] = mapped_column("DS_OUTPUT_DIR", String(1000), nullable=True)
    schema_explore: Mapped[Optional[str]] = mapped_column("DS_SCHEMA_EXPLORE", String(1000), nullable=True)
    all_schemas: Mapped[bool] = mapped_column("FL_ALL_SCHEMAS", Boolean, default=False)
    meta_file_path: Mapped[Optional[str]] = mapped_column("DS_META_FILE_PATH", String(1000), nullable=True)
    description: Mapped[Optional[str]] = mapped_column("DE_DESCRIPTION", String(2000), nullable=True)
    table_name_regex: Mapped[Optional[str]] = mapped_column("DS_TABLE_NAME_REGEX", String(500), nullable=True)
    table_exclusion_regex: Mapped[Optional[str]] = mapped_column("DS_TABLE_EXCLUSION_REGEX", String(500), nullable=True)
    column_exclusion_regex: Mapped[Optional[str]] = mapped_column("DS_COLUMN_EXCLUSION_REGEX", String(500), nullable=True)
    excluded_relationships: Mapped[bool] = mapped_column("FL_EXCLUDED_RELATIONSHIPS", Boolean, default=False)
    charset: Mapped[Optional[str]] = mapped_column("CD_CHARSET", String(50), nullable=True)
    font_name: Mapped[Optional[str]] = mapped_column("NM_FONT", String(100), nullable=True)
    font_size: Mapped[Optional[str]] = mapped_column("NR_FONT_SIZE", String(50), nullable=True)
    css_path: Mapped[Optional[str]] = mapped_column("DS_CSS_PATH", String(1000), nullable=True)

    # New parameters for SchemaSpy v6.1.0
    schemas_list: Mapped[Optional[str]] = mapped_column("DS_SCHEMAS_LIST", String(1000), nullable=True)
    catalog_filter: Mapped[Optional[str]] = mapped_column("DS_CATALOG_FILTER", String(255), nullable=True)
    renderer: Mapped[Optional[str]] = mapped_column("NM_RENDERER", String(100), nullable=True)
    image_format: Mapped[Optional[str]] = mapped_column("CD_IMAGE_FORMAT", String(50), nullable=True)
    degree_of_separation: Mapped[Optional[int]] = mapped_column("NR_DEGREE_OF_SEPARATION", Integer, nullable=True)
    graphviz_path: Mapped[Optional[str]] = mapped_column("DS_GRAPHVIZ_PATH", String(1000), nullable=True)
    connection_properties: Mapped[Optional[str]] = mapped_column("DS_CONNECTION_PROPERTIES", String(1000), nullable=True)
    language: Mapped[Optional[str]] = mapped_column("CD_LANGUAGE", String(50), nullable=True)
    verbose: Mapped[bool] = mapped_column("FL_VERBOSE", Boolean, default=False)
    quiet: Mapped[bool] = mapped_column("FL_QUIET", Boolean, default=False)
    post_processing: Mapped[Optional[str]] = mapped_column("DS_POST_PROCESSING", String(1000), nullable=True)
    prompt_password: Mapped[bool] = mapped_column("FL_PROMPT_PASSWORD", Boolean, default=False)
    vizjs: Mapped[bool] = mapped_column("FL_VIZJS", Boolean, default=False)
