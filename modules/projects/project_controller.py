# Artefato:  project_controller.py

import json
from PyQt6.QtWidgets import QFileDialog
from .project_viewmodel import ProjectViewModel
from .project_dto import ProjectDTO
from .import_dialog import ImportProjectsDialog
from .project_validator import ProjectValidator
from modules.connections.connection_dto import ConnectionDTO
from shared.services.config_service import ConfigService

class ProjectController:

    def __init__(self, view, viewmodel: ProjectViewModel, connection_service=None):
        self.view = view
        self.viewmodel = viewmodel
        self.connection_service = connection_service
        self.on_data_changed_callbacks = []
        self._connect_signals()
        self.read_project()

    def _connect_signals(self):
        # Botões
        self.view.btn_new.clicked.connect(self.new_project)
        self.view.btn_save.clicked.connect(self.save_project)
        self.view.btn_delete.clicked.connect(self.delete_project)
        self.view.btn_import.clicked.connect(self.import_projects)
        # Seleção da Grid
        self.view.project_selected.connect(self.select_project)
    
    def validate_form(self):
        dto = self.view.get_project()
        validator = ProjectValidator()
        report = validator.validate(dto)

        if not report.valid:
            self.view.show_validation(report)
            self.view.txt_projeto.setFocus()
            return False

        return True

    def new_project(self):
        self.view.clear_form()

    def read_project(self):
        try:
            project = (self.viewmodel.read_project())
            self.view.populate_grid(project)
        except Exception as ex:
            self.view.show_error_message("Project Controller - Load", str(ex))

    def save_project(self):
        try:
            if not self.validate_form():
                return

            dto = self.view.get_project()

            if self.view.current_project_id:
                self.viewmodel.update_project(dto)            
            else:                
                self.viewmodel.create_project(dto)
            
            self.view.show_message("Sucesso", "Projeto salvo com sucesso.")
            
            self.read_project()
            self.view.clear_form()
        except Exception as ex:
            self.view.show_error_message("Project Controller - Save", str(ex))

    def delete_project(self):
        try:
            id_projeto = (self.view.get_selected_id_projeto())
            if not id_projeto:
                self.view.show_warning_message("Aviso", "Selecione um projeto.")
                return

            if not self.view.show_question_message("Confirmação", "Deseja excluir o projeto?"):
                return

            self.viewmodel.delete_project(id_projeto)

            self.view.show_message("Sucesso", "Projeto excluído.")

            self.read_project()
            self.view.clear_form()

        except Exception as ex:
            self.view.show_error_message("Project Controller - Delete", str(ex))

    def select_project(self, id_projeto):
        try:
            project = (self.viewmodel.get_project_by_id(id_projeto))
            self.view.load_project(project)
        except Exception as ex:
            self.view.show_error_message("Project Controller - Select", str(ex))

    # BUG FIX: Implementação - Método de importação em lote a partir do diálogo modal
    def import_projects(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.view,
                "Importar Projetos (JSON)",
                "",
                "Arquivos JSON (*.json)"
            )
            if not file_path:
                return

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # BUG FIX: Implementação - Desaninhar coleções do JSON se for dicionário de primeiro nível
            if isinstance(data, dict):
                extracted_list = None
                # 1. Tentar encontrar uma chave contendo uma lista direta de objetos
                for key, val in data.items():
                    if isinstance(val, list):
                        extracted_list = val
                        break
                # 2. Se não encontrou lista, tentar encontrar chaves como "connections", "projects" ou "items"
                # que contenham um dicionário de objetos (como no DBeaver)
                if extracted_list is None:
                    for key, val in data.items():
                        if isinstance(val, dict) and key in ("connections", "projects", "items"):
                            extracted_list = list(val.values())
                            break
                            
                if extracted_list is not None:
                    data = extracted_list
                else:
                    data = [data]

            if not isinstance(data, list):
                self.view.show_error_message("Erro de Formato", "O arquivo JSON deve conter um projeto ou uma lista de projetos.")
                return

            dialog = ImportProjectsDialog(data, parent=self.view)
            if dialog.exec() == ImportProjectsDialog.DialogCode.Accepted:
                imported_items = dialog.get_imported_projects()
                
                # Carregar databases do ConfigService
                databases = ConfigService.load_databases()
                
                success_count = 0
                duplicate_count = 0
                for proj_data, raw_item in imported_items:
                    # 1. Extrair os dados mapeados e finais do projeto/conexão
                    nm_projeto = proj_data["nm_projeto"]
                    tp_database = proj_data["tp_database"]
                    nm_host = proj_data["nm_host"]
                    nu_porta = proj_data["nu_porta"]
                    nm_database = proj_data["nm_database"]
                    nm_schema = proj_data["nm_schema"]
                    nm_usuario = proj_data["nm_usuario"]
                    tx_password = proj_data["tx_password"]
                    ds_caminho = proj_data["ds_caminho"]
                    ds_jdbc_driver = proj_data["ds_jdbc_driver"]
                    ds_jdbc_url = proj_data["ds_jdbc_url"]
                    
                    nm_conexao = nm_projeto # O nome da conexão segue o do projeto
                    
                    # 2. Verificar duplicidade de conexões na base de dados
                    if self.connection_service:
                        is_duplicate = self.connection_service.check_duplicate(
                            nm_conexao=nm_conexao,
                            tp_database=tp_database,
                            nm_host=nm_host,
                            nu_porta=nu_porta,
                            nm_database=nm_database,
                            nm_schema=nm_schema,
                            nm_usuario=nm_usuario,
                            tx_password=tx_password,
                            ds_caminho=ds_caminho
                        )
                        if is_duplicate:
                            duplicate_count += 1
                            continue # Ignora conexões duplicadas
                    
                    # 3. Criar ou atualizar o Projeto no módulo Projeto evitando erros de UNIQUE constraint
                    project_entity = self.viewmodel.get_project_by_name(nm_projeto)
                    if project_entity:
                        id_projeto = project_entity.id_projeto
                        # Compara todos os campos para verificar duplicidade ou se necessita de atualização
                        if (project_entity.tp_database != tp_database or
                            project_entity.nm_database != nm_database or
                            project_entity.nm_host != nm_host or
                            project_entity.nm_schema != nm_schema or
                            project_entity.nu_porta != nu_porta):
                            
                            dto_projeto = ProjectDTO(
                                id_projeto=id_projeto,
                                nm_projeto=nm_projeto,
                                tp_database=tp_database,
                                nm_database=nm_database,
                                nm_host=nm_host,
                                nm_schema=nm_schema,
                                nu_porta=nu_porta
                            )
                            self.viewmodel.update_project(dto_projeto)
                    else:
                        dto_projeto = ProjectDTO(
                            nm_projeto=nm_projeto,
                            tp_database=tp_database,
                            nm_database=nm_database,
                            nm_host=nm_host,
                            nm_schema=nm_schema,
                            nu_porta=nu_porta
                        )
                        project_entity = self.viewmodel.create_project(dto_projeto)
                        id_projeto = project_entity.id_projeto
                    
                    # 4. Gerar Driver e URL JDBC se não vierem diretamente mapeados/preenchidos
                    if not ds_jdbc_url or not ds_jdbc_driver:
                        db_config = next((db for db in databases if db["name"] == tp_database), None)
                        if db_config:
                            if not ds_jdbc_driver:
                                ds_jdbc_driver = db_config.get("driver_class", "")
                            if not ds_jdbc_url:
                                url_template = db_config.get("url_template", "")
                                host = nm_host or ""
                                port = str(nu_porta) if nu_porta is not None else ""
                                db_name = nm_database or ""
                                schema_name = nm_schema or ""
                                user_name = nm_usuario or ""
                                pass_val = tx_password or ""
                                ds_jdbc_url = url_template.replace("<host>", host).replace("<port>", port).replace("<database>", db_name).replace("<schema>", schema_name).replace("<user>", user_name).replace("<password>", pass_val).replace("<caminho>", ds_caminho)

                    # 5. Criar a Conexão associada ao Projeto
                    if self.connection_service:
                        dto_conexao = ConnectionDTO(
                            id_projeto=id_projeto,
                            nm_conexao=nm_conexao,
                            tp_database=tp_database,
                            nm_host=nm_host,
                            nu_porta=nu_porta,
                            nm_database=nm_database,
                            nm_schema=nm_schema,
                            nm_usuario=nm_usuario,
                            tx_password=tx_password,
                            ds_caminho=ds_caminho,
                            ds_jdbc_driver=ds_jdbc_driver,
                            ds_jdbc_url=ds_jdbc_url,
                            fl_ativo=True
                        )
                        self.connection_service.create_connection(dto_conexao)
                    
                    success_count += 1
                
                msg = f"{success_count} projeto(s) e conexão(ões) importados com sucesso."
                if duplicate_count > 0:
                    msg += f"\n({duplicate_count} conexão(ões) duplicada(s) ignorada(s))."
                self.view.show_message("Importação Concluída", msg)
                self.read_project()
                self.view.clear_form()
                
                # BUG FIX: Implementação - Disparar callbacks de dados alterados para recarregar módulos dependentes (como conexões)
                for callback in self.on_data_changed_callbacks:
                    try:
                        callback()
                    except Exception:
                        pass

        except Exception as ex:
            self.view.show_error_message("Project Controller - Import", str(ex))
