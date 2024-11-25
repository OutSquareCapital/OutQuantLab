from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTabWidget, QPushButton, QWidget, QHBoxLayout
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

class MainWindow(QMainWindow):
    def __init__(self, param_config, asset_config, assets_names, methods_config):
        super().__init__()
        self.setWindowTitle("Main Configuration")
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
        save_exit_button = QPushButton("Exit")
        save_exit_button.setEnabled(False)
        save_exit_button.clicked.connect(self.save_and_exit)
        button_layout.addStretch()
        button_layout.addWidget(save_exit_button)
        main_layout.addLayout(button_layout)

        # Connecter les signaux des widgets
        self.param_widget.parameters_saved.connect(lambda: self.check_all_saved(save_exit_button))
        self.asset_widget.assets_saved.connect(lambda: self.check_all_saved(save_exit_button))
        self.method_widget.methods_saved.connect(lambda: self.check_all_saved(save_exit_button))

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def check_all_saved(self, button: QPushButton):
        if (
            not self.param_widget.apply_button.isEnabled()
            and not self.asset_widget.apply_button.isEnabled()
            and not self.method_widget.apply_button.isEnabled()
        ):
            button.setEnabled(True)

    def save_and_exit(self):
        self.param_config = self.param_widget.get_data()
        self.asset_config = self.asset_widget.get_data()
        self.methods_config = self.method_widget.get_data()
        self.active_methods = self.method_widget.get_active_methods()
        self.close()

    def get_results(self):
        return self.param_config, self.asset_config, self.active_methods

def dynamic_config(assets_names, auto=True):
    
    param_config = load_param_config()
    asset_config = load_assets_to_backtest_config()
    methods_config = load_methods_config()

    if auto:
        active_methods = get_active_methods(methods_config)
        indicators_and_params = automatic_generation(active_methods, param_config)
        return indicators_and_params, asset_config

    app = QApplication([])
    window = MainWindow(param_config, asset_config, assets_names, methods_config)
    window.show()
    app.exec()

    active_methods = get_active_methods(window.methods_config)
    indicators_and_params = automatic_generation(active_methods, param_config)
    return indicators_and_params, window.asset_config