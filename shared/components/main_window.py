# main_window.py

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)

from PyQt6.QtGui import QIcon

from infrastructure.database import (
    SessionLocal
)

from shared.components.sidebar    import SideBar
from shared.components.top_menu   import TopMenu
from shared.components.status_bar import AppStatusBar

# Dashboard
from modules.dashboard.dashboard_view     import DashboardView
# Projetos
from modules.projects import (
    ProjectRepository,
    ProjectService,
    ProjectViewModel,
    ProjectController,
    ProjectView
)
# Conexões
from modules.connections import (
    ConnectionRepository,
    ConnectionService,
    ConnectionViewModel,
    ConnectionController,
    ConnectionView
)
# Execução
from modules.execution.execution_view    import ExecutionView
# Histórico
from modules.history.history_view        import HistoryView
# Configurações
from modules.settings import (
    SettingRepository,
    SettingService,
    SettingViewModel,
    SettingController,
    SettingView
)
# Sobre
from modules.about.about_view            import AboutView

from core.navigation.navigation_service import NavigationService

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SchemaSpy GUI")
        self.setWindowIcon(
            QIcon("resources/icons/schemaspygui.ico")
        )
        self.resize(1400, 900)
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        self.top_menu = TopMenu()
        root_layout.addWidget(self.top_menu)
        content_layout = QHBoxLayout()
        self.sidebar = SideBar()
        content_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        root_layout.addLayout(content_layout)
        self.setStatusBar(AppStatusBar())
        
        # Navigation
        self.navigation = NavigationService(self.stack)
        
        # Dashboard
        dashboard_view = DashboardView()
        self.navigation.register_page("dashboard", dashboard_view)
                
        # Conexão (Instanciar serviço mais cedo para o ProjectController)
        self.connection_session = SessionLocal()
        connection_repository = ConnectionRepository(self.connection_session)
        connection_service = ConnectionService(connection_repository)

        # Projetos
        project_view = ProjectView()
        self.project_session = SessionLocal()
        project_repository = ProjectRepository(self.project_session)
        project_service = ProjectService(project_repository)
        project_viewmodel = ProjectViewModel(project_service)
        self.project_controller = ProjectController(project_view, project_viewmodel, connection_service=connection_service)
        self.navigation.register_page("project", project_view)
        
        # Conexão (View, ViewModel e Controller)
        connection_view = ConnectionView()
        connection_viewmodel = ConnectionViewModel(connection_service)
        self.connection_controller = ConnectionController(connection_view, connection_viewmodel, project_service=project_service)
        self.navigation.register_page("connection", connection_view)

        # BUG FIX: Alteração - Ligar callback de dados alterados para recarregar as conexões na grid
        self.project_controller.on_data_changed_callbacks.append(self.connection_controller.read_connection)
        
        # Execução
        execution_view = ExecutionView()
        self.navigation.register_page("execution", execution_view)

        # Histórico
        history_view = HistoryView()
        self.navigation.register_page("history", history_view)

        # Configurações
        setting_view = SettingView()
        self.setting_session = SessionLocal()
        setting_repository = SettingRepository(self.setting_session)
        setting_service = SettingService(setting_repository)
        setting_viewmodel = SettingViewModel(setting_service)
        self.setting_controller = SettingController(setting_view, setting_viewmodel, connection_service=connection_service)
        self.navigation.register_page("setting", setting_view)

        # Regerar dados de configurações quando houver alteração de projetos ou conexões
        self.project_controller.on_data_changed_callbacks.append(self.setting_controller.read_setting)
        self.connection_controller.on_data_changed_callbacks.append(self.setting_controller.read_setting)

        # Sobre
        about_view = AboutView()
        self.navigation.register_page("about", about_view)

        self.sidebar.navigate_requested.connect(self.navigation.navigate)
        
        self.navigation.navigate("dashboard")

    def closeEvent(self, event):
        """
        Melhoria de arquitetura: Garante o fechamento limpo das sessões de banco ao fechar a janela,
        evitando locks do SQLite e liberando recursos.
        """
        try:
            if hasattr(self, 'project_session') and self.project_session:
                self.project_session.close()
        except Exception:
            pass
        try:
            if hasattr(self, 'connection_session') and self.connection_session:
                self.connection_session.close()
        except Exception:
            pass
        try:
            if hasattr(self, 'setting_session') and self.setting_session:
                self.setting_session.close()
        except Exception:
            pass
        super().closeEvent(event)
