
from typing import Dict, List
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QWidget, QScrollArea, QLabel
)
from .Dynamic_Config_Backend import save_assets_to_backtest_config, load_assets_to_backtest_config

def select_assets(assets_names: List[str], auto: bool = True) -> Dict[str, List[str]]:

    if auto:
        return load_assets_to_backtest_config()

    else: 
        current_config = load_assets_to_backtest_config()
        app = QApplication([])

        class AssetSelectionWindow(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Assets to backtest selection")
                self.current_config = current_config
                self.category_vars = {}
                self.select_all_buttons = {}
                self.unselect_all_buttons = {}
                self.validation_label = None
                self.apply_button = None
                self.restricted_keys = ['ratios', 'ensembles', 'canary_ratios', 'canary_ensembles']
                self.init_ui()

            def init_ui(self):
                main_widget = QWidget()
                main_layout = QVBoxLayout()
                scroll_area = QScrollArea()
                scroll_widget = QWidget()
                scroll_layout = QHBoxLayout()

                # Création des catégories et des cases à cocher
                for category in self.current_config.keys():
                    category_box = QGroupBox(category)
                    category_layout = QVBoxLayout()

                    # Boutons "Select All" et "Unselect All"
                    button_layout = QHBoxLayout()
                    select_all_button = QPushButton("Select All")
                    unselect_all_button = QPushButton("Unselect All")

                    select_all_button.clicked.connect(lambda _, c=category: self.select_all(c))
                    unselect_all_button.clicked.connect(lambda _, c=category: self.unselect_all(c))

                    button_layout.addWidget(select_all_button)
                    button_layout.addWidget(unselect_all_button)
                    category_layout.addLayout(button_layout)

                    self.select_all_buttons[category] = select_all_button
                    self.unselect_all_buttons[category] = unselect_all_button

                    # Actifs individuels
                    self.category_vars[category] = {}
                    for asset in assets_names:
                        asset_checkbox = QCheckBox(asset)
                        asset_checkbox.setChecked(asset in self.current_config.get(category, []))
                        asset_checkbox.stateChanged.connect(self.validate_config)
                        self.category_vars[category][asset] = asset_checkbox
                        category_layout.addWidget(asset_checkbox)

                    category_box.setLayout(category_layout)
                    scroll_layout.addWidget(category_box)

                scroll_widget.setLayout(scroll_layout)
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)
                main_layout.addWidget(scroll_area)

                # Bouton "Apply selection"
                self.apply_button = QPushButton("Apply selection")
                self.apply_button.clicked.connect(self.save_selection)
                self.apply_button.setEnabled(False)
                main_layout.addWidget(self.apply_button)

                # Label pour afficher les messages d'avertissement
                self.validation_label = QLabel("")
                self.validation_label.setStyleSheet("color: red;")
                main_layout.addWidget(self.validation_label)

                main_widget.setLayout(main_layout)
                self.setCentralWidget(main_widget)

                # Initialiser l'état des boutons et valider la configuration
                for category in self.current_config.keys():
                    self.update_buttons_state(category)
                self.validate_config()

            def update_buttons_state(self, category: str):
                # Vérifie si tous les actifs sont sélectionnés ou aucun
                all_selected = all(var.isChecked() for var in self.category_vars[category].values())
                none_selected = not any(var.isChecked() for var in self.category_vars[category].values())

                # Activer/désactiver les boutons en conséquence
                self.select_all_buttons[category].setEnabled(not all_selected)
                self.unselect_all_buttons[category].setEnabled(not none_selected)

            def select_all(self, category: str):
                for var in self.category_vars[category].values():
                    var.setChecked(True)
                self.update_buttons_state(category)
                self.validate_config()

            def unselect_all(self, category: str):
                for var in self.category_vars[category].values():
                    var.setChecked(False)
                self.update_buttons_state(category)
                self.validate_config()

            def validate_config(self):
                # Vérifie les restrictions spécifiques pour les catégories
                for key in self.restricted_keys:
                    if key in self.category_vars:
                        selected_assets = [asset for asset, var in self.category_vars[key].items() if var.isChecked()]
                        if len(selected_assets) == 1:
                            self.validation_label.setText(f"Error: '{key}' cannot contain exactly 1 asset.")
                            self.apply_button.setEnabled(False)
                            return

                # Si tout est valide, activer le bouton
                self.validation_label.setText("")
                self.apply_button.setEnabled(True)

            def save_selection(self):
                for category, asset_vars in self.category_vars.items():
                    self.current_config[category] = [asset for asset, var in asset_vars.items() if var.isChecked()]
                save_assets_to_backtest_config(self.current_config)
                self.close()

        window = AssetSelectionWindow()
        window.show()
        app.exec()
        return window.current_config