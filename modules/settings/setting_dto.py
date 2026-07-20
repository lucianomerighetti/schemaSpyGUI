# setting_dto.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class SettingDTO:
    """DTO utilizado pelo módulo de configurações."""

    id_setting: Optional[int] = None
    nm_setting: str = ""
    id_conexao: Optional[int] = None

    # Tab 2: Parameters/Flags Form
    db_driver_path: str = ""
    schemaspy_path: str = ""
    properties_path: str = ""
    properties_text: str = ""
    high_quality: bool = False
    low_quality: bool = False
    single_sign_on: bool = False
    show_finish: bool = False
    a_html: bool = False
    no_html: bool = False
    dinc_fk: bool = False
    no_ads: bool = False
    no_logo: bool = False
    no_rows: bool = False
    rails: bool = False

    # Tab 3: Output Options Form
    output_dir: str = ""
    schema_explore: str = ""
    all_schemas: bool = False
    meta_file_path: str = ""
    description: str = ""
    table_name_regex: str = ""
    table_exclusion_regex: str = ""
    column_exclusion_regex: str = ""
    excluded_relationships: bool = False
    charset: str = ""
    font_name: str = ""
    font_size: str = ""
    css_path: str = ""

    # New parameters for SchemaSpy v6.1.0
    schemas_list: str = ""
    catalog_filter: str = ""
    renderer: str = ""
    image_format: str = ""
    degree_of_separation: Optional[int] = None
    graphviz_path: str = ""
    connection_properties: str = ""
    language: str = ""
    verbose: bool = False
    quiet: bool = False
    post_processing: str = ""
    prompt_password: bool = False

    @property
    def is_new(self) -> bool:
        return self.id_setting is None
