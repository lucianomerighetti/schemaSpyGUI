# setting_service.py
from shared.services.base_service import BaseService
from .setting import Setting
from .setting_dto import SettingDTO

class SettingService(BaseService):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def get_settings(self):
        return self.repository.get_all()

    def create_setting(self, dto: SettingDTO):
        setting = Setting(
            nm_setting=dto.nm_setting,
            id_conexao=dto.id_conexao,
            db_driver_path=dto.db_driver_path,
            schemaspy_path=dto.schemaspy_path,
            properties_path=dto.properties_path,
            properties_text=dto.properties_text,
            high_quality=dto.high_quality,
            low_quality=dto.low_quality,
            single_sign_on=dto.single_sign_on,
            show_finish=dto.show_finish,
            a_html=dto.a_html,
            no_html=dto.no_html,
            dinc_fk=dto.dinc_fk,
            no_ads=dto.no_ads,
            no_logo=dto.no_logo,
            no_rows=dto.no_rows,
            rails=dto.rails,
            output_dir=dto.output_dir,
            schema_explore=dto.schema_explore,
            all_schemas=dto.all_schemas,
            meta_file_path=dto.meta_file_path,
            description=dto.description,
            table_name_regex=dto.table_name_regex,
            table_exclusion_regex=dto.table_exclusion_regex,
            column_exclusion_regex=dto.column_exclusion_regex,
            excluded_relationships=dto.excluded_relationships,
            charset=dto.charset,
            font_name=dto.font_name,
            font_size=dto.font_size,
            css_path=dto.css_path,
            schemas_list=dto.schemas_list,
            catalog_filter=dto.catalog_filter,
            renderer=dto.renderer,
            image_format=dto.image_format,
            degree_of_separation=dto.degree_of_separation,
            graphviz_path=dto.graphviz_path,
            connection_properties=dto.connection_properties,
            language=dto.language,
            verbose=dto.verbose,
            quiet=dto.quiet,
            post_processing=dto.post_processing,
            prompt_password=dto.prompt_password,
            vizjs=dto.vizjs
        )
        return self.repository.create(setting)

    def update_setting(self, dto: SettingDTO):
        setting = self.repository.get_by_id(dto.id_setting)
        if not setting:
            raise Exception("Configuração não encontrada.")

        setting.nm_setting = dto.nm_setting
        setting.id_conexao = dto.id_conexao
        setting.db_driver_path = dto.db_driver_path
        setting.schemaspy_path = dto.schemaspy_path
        setting.properties_path = dto.properties_path
        setting.properties_text = dto.properties_text
        setting.high_quality = dto.high_quality
        setting.low_quality = dto.low_quality
        setting.single_sign_on = dto.single_sign_on
        setting.show_finish = dto.show_finish
        setting.a_html = dto.a_html
        setting.no_html = dto.no_html
        setting.dinc_fk = dto.dinc_fk
        setting.no_ads = dto.no_ads
        setting.no_logo = dto.no_logo
        setting.no_rows = dto.no_rows
        setting.rails = dto.rails
        setting.output_dir = dto.output_dir
        setting.schema_explore = dto.schema_explore
        setting.all_schemas = dto.all_schemas
        setting.meta_file_path = dto.meta_file_path
        setting.description = dto.description
        setting.table_name_regex = dto.table_name_regex
        setting.table_exclusion_regex = dto.table_exclusion_regex
        setting.column_exclusion_regex = dto.column_exclusion_regex
        setting.excluded_relationships = dto.excluded_relationships
        setting.charset = dto.charset
        setting.font_name = dto.font_name
        setting.font_size = dto.font_size
        setting.css_path = dto.css_path
        setting.schemas_list = dto.schemas_list
        setting.catalog_filter = dto.catalog_filter
        setting.renderer = dto.renderer
        setting.image_format = dto.image_format
        setting.degree_of_separation = dto.degree_of_separation
        setting.graphviz_path = dto.graphviz_path
        setting.connection_properties = dto.connection_properties
        setting.language = dto.language
        setting.verbose = dto.verbose
        setting.quiet = dto.quiet
        setting.post_processing = dto.post_processing
        setting.prompt_password = dto.prompt_password
        setting.vizjs = dto.vizjs
 
        self.repository.update()

    def delete_setting(self, id_setting: int):
        setting = self.repository.get_by_id(id_setting)
        if not setting:
            raise Exception("Configuração não encontrada.")
        self.repository.delete(setting)

    def get_setting_by_id(self, id_setting: int):
        return self.repository.get_by_id(id_setting)

    def get_setting_by_name(self, nm_setting: str):
        return self.repository.get_by_name(nm_setting)
