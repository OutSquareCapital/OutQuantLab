from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QTabWidget, QPushButton, QWidget, QHBoxLayout
from .Config_Params import ParameterWidget
from .Config_Assets import AssetSelectionWidget
from .Config_Indicators import MethodSelectionWidget
from .Config_Backend import (
    load_param_config, 
    load_assets_to_backtest_config, 
    load_methods_config,
    get_active_methods
)
from .Strategy_Params_Generation import automatic_generation

class ConfigApp(QMainWindow):
    def __init__(self, param_config, asset_config, assets_names, methods_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.param_config = param_config
        self.asset_config = asset_config
        self.assets_names = assets_names
        self.methods_config = methods_config    
        self.param_widget = None
        self.asset_widget = None
        self.method_widget = None
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Onglets
        self.tabs = QTabWidget()
        self.param_widget = ParameterWidget(self.param_config)
        self.asset_widget = AssetSelectionWidget(self.asset_config, self.assets_names)
        self.method_widget = MethodSelectionWidget(self.methods_config)

        self.tabs.addTab(self.param_widget, "Edit Parameters")
        self.tabs.addTab(self.asset_widget, "Edit Assets")
        self.tabs.addTab(self.method_widget, "Edit Indicators")
        main_layout.addWidget(self.tabs)

        # Bouton Save & Exit
        button_layout = QHBoxLayout()
        exit_button = QPushButton("Close")
        exit_button.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(exit_button)
        main_layout.addLayout(button_layout)

        # Connecter les signaux des widgets
        self.param_widget.parameters_saved.connect(lambda: self.check_all_saved(exit_button))
        self.asset_widget.assets_saved.connect(lambda: self.check_all_saved(exit_button))
        self.method_widget.methods_saved.connect(lambda: self.check_all_saved(exit_button))

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def check_all_saved(self, button: QPushButton):
        if (
            not self.param_widget.apply_button.isEnabled()
            and not self.asset_widget.apply_button.isEnabled()
            and not self.method_widget.apply_button.isEnabled()
        ):
            button.setEnabled(True)

    def get_results(self):
        return self.param_widget.get_data(), self.asset_widget.get_data(), self.method_widget.get_active_methods()


def dynamic_config(assets_names, auto=True, parent=None):
    param_config = load_param_config()
    asset_config = load_assets_to_backtest_config()
    methods_config = load_methods_config()

    if auto:
        active_methods = get_active_methods(methods_config)
        indicators_and_params = automatic_generation(active_methods, param_config)
        return indicators_and_params, asset_config

    window = ConfigApp(param_config, asset_config, assets_names, methods_config, parent=parent)
    window.show()
