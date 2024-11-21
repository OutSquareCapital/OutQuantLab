from typing import Dict, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QScrollArea, QLabel
)
from PySide6.QtCore import Signal
from .Config_Backend import save_assets_to_backtest_config

class AssetSelectionWidget(QWidget):
    assets_saved = Signal()  # Signal pour indiquer que les actifs ont été sauvegardés

    def __init__(self, current_config: Dict[str, List[str]], assets_names: List[str]):
        super().__init__()
        self.current_config = current_config
        self.assets_names = assets_names
        self.category_vars = {}
        self.select_all_buttons = {}
        self.unselect_all_buttons = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout()

        for category in self.current_config.keys():
            category_box = self.create_category_box(category)
            scroll_layout.addWidget(category_box)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Bouton "Apply"
        self.apply_button = QPushButton("Apply selection")
        self.apply_button.setEnabled(False)  # Grisé au départ
        self.apply_button.clicked.connect(self.save_selection)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)
        self.initialize_button_states()

    def create_category_box(self, category: str) -> QGroupBox:
        category_box = QGroupBox(category)
        category_layout = QVBoxLayout()

        # Boutons "Select All" et "Unselect All"
        button_layout, select_button, unselect_button = self.create_category_buttons(category)
        category_layout.addLayout(button_layout)

        # Sauvegarde des boutons
        self.select_all_buttons[category] = select_button
        self.unselect_all_buttons[category] = unselect_button

        # Checkboxes pour les actifs
        self.category_vars[category] = {}
        for asset in self.assets_names:
            asset_checkbox = self.create_asset_checkbox(category, asset)
            category_layout.addWidget(asset_checkbox)

        category_box.setLayout(category_layout)
        return category_box

    def create_category_buttons(self, category: str) -> tuple:
        button_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        unselect_all_button = QPushButton("Unselect All")

        select_all_button.clicked.connect(lambda _, c=category: self.select_all(c))
        unselect_all_button.clicked.connect(lambda _, c=category: self.unselect_all(c))

        button_layout.addWidget(select_all_button)
        button_layout.addWidget(unselect_all_button)
        return button_layout, select_all_button, unselect_all_button

    def create_asset_checkbox(self, category: str, asset: str) -> QCheckBox:
        asset_checkbox = QCheckBox(asset)
        asset_checkbox.setChecked(asset in self.current_config.get(category, []))
        asset_checkbox.stateChanged.connect(lambda _: self.update_buttons_state(category))
        asset_checkbox.stateChanged.connect(self.enable_apply_button)
        self.category_vars[category][asset] = asset_checkbox
        return asset_checkbox

    def enable_apply_button(self):
        self.apply_button.setEnabled(True)  # Activer le bouton Apply dès qu'un changement est détecté

    def save_selection(self):
        for category, asset_vars in self.category_vars.items():
            self.current_config[category] = [asset for asset, var in asset_vars.items() if var.isChecked()]
        save_assets_to_backtest_config(self.current_config)
        self.apply_button.setEnabled(False)  # Désactiver le bouton après sauvegarde
        self.assets_saved.emit()

    def select_all(self, category: str):
        for var in self.category_vars[category].values():
            var.setChecked(True)
        self.update_buttons_state(category)
        self.enable_apply_button()

    def unselect_all(self, category: str):
        for var in self.category_vars[category].values():
            var.setChecked(False)
        self.update_buttons_state(category)
        self.enable_apply_button()

    def initialize_button_states(self):
        for category in self.current_config.keys():
            self.update_buttons_state(category)

    def update_buttons_state(self, category: str):
        all_selected = all(var.isChecked() for var in self.category_vars[category].values())
        none_selected = not any(var.isChecked() for var in self.category_vars[category].values())

        self.select_all_buttons[category].setEnabled(not all_selected)
        self.unselect_all_buttons[category].setEnabled(not none_selected)

    def get_data(self) -> Dict[str, List[str]]:
        return self.current_config
