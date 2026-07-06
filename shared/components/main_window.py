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
# COnfigurações
from modules.settings.settings_view      import SettingView
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
                
        # Projetos
        project_view = ProjectView()
        project_repository = ProjectRepository(SessionLocal())
        project_service = ProjectService(project_repository)
        project_viewmodel = ProjectViewModel(project_service)
        self.project_controller = ProjectController(project_view, project_viewmodel)
        self.navigation.register_page("project", project_view)
        
        # Conexão
        connection_view = ConnectionView()
        self.navigation.register_page("connection", connection_view)
        
        # Execução
        execution_view = ExecutionView()
        self.navigation.register_page("execution", execution_view)

        # Histórico
        history_view = HistoryView()
        self.navigation.register_page("history", history_view)

        # Configurações
        setting_view = SettingView()
        self.navigation.register_page("setting", setting_view)

        # Sobre
        about_view = AboutView()
        self.navigation.register_page("about", about_view)


        self.sidebar.navigate_requested.connect(self.navigation.navigate)
        
        self.navigation.navigate("dashboard")
