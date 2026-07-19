# sidebar.py

from PyQt6.QtCore    import pyqtSignal
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout


class SideBar(QWidget):

    navigate_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout()

        self.bt_dashboard   = QPushButton("📊 Dashboard")
        self.bt_projects    = QPushButton("📁 Projetos")
        self.bt_connections = QPushButton("🔗 Conexões")
        self.bt_settings    = QPushButton("🔧 Configurações")
        self.bt_execution   = QPushButton("🚀 Execuções")
        self.bt_history     = QPushButton("📜 Histórico")
        self.bt_about       = QPushButton("ℹ️ Sobre")
        self.bt_quit        = QPushButton("❌ Sair")

        layout.addWidget(self.bt_dashboard)
        layout.addWidget(self.bt_projects)
        layout.addWidget(self.bt_connections)
        layout.addWidget(self.bt_settings)
        layout.addWidget(self.bt_execution)
        layout.addWidget(self.bt_history)
        layout.addWidget(self.bt_about)
        layout.addWidget(self.bt_quit)

        layout.addStretch()

        self.setLayout(layout)

        self.bt_dashboard.clicked.connect(lambda: self.navigate_requested.emit("dashboard"))
        self.bt_projects.clicked.connect(lambda: self.navigate_requested.emit("project"))
        self.bt_connections.clicked.connect(lambda: self.navigate_requested.emit("connection"))
        self.bt_execution.clicked.connect(lambda: self.navigate_requested.emit("execution"))
        self.bt_history.clicked.connect(lambda: self.navigate_requested.emit("history"))
        self.bt_settings.clicked.connect(lambda: self.navigate_requested.emit("setting"))
        self.bt_about.clicked.connect(lambda: self.navigate_requested.emit("about"))
        
        # BUG FIX: Implementação - Botão Sair encerrando a aplicação PyQt6 de forma limpa
        from PyQt6.QtWidgets import QApplication
        self.bt_quit.clicked.connect(QApplication.instance().quit)