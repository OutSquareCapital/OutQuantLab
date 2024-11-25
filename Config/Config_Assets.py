from typing import Dict, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QScrollArea, QLabel
)
from PySide6.QtCore import Signal
from .Config_Backend import save_assets_to_backtest_config

class AssetSelectionWidget(QWidget):
    assets_saved = Signal()

    def __init__(self, current_config: Dict[str, List[str]], assets_names: List[str]):
        super().__init__()
        self.current_config = current_config
        self.assets_names = assets_names
        self.category_vars = {}
        self.select_all_buttons = {}
        self.unselect_all_buttons = {}
        self.warning_labels = {} 
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

        # Labels d'avertissement spécifiques (en dehors des catégories)
        for category in ["ratios", "ensembles"]:
            warning_label = QLabel(f"At least two assets must be selected in '{category}'")
            warning_label.setStyleSheet("color: red;")
            warning_label.setVisible(False)  # Caché au départ
            self.warning_labels[category] = warning_label
            layout.addWidget(warning_label)

        # Bouton "Apply"
        self.apply_button = QPushButton("Apply selection")
        self.apply_button.setEnabled(False)  # Grisé au départ
        self.apply_button.clicked.connect(self.save_selection)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)


    def create_asset_checkbox(self, category: str, asset: str) -> QCheckBox:
        asset_checkbox = QCheckBox(asset)
        asset_checkbox.setChecked(asset in self.current_config.get(category, []))
        asset_checkbox.stateChanged.connect(self.check_asset_count)  # Vérification dynamique
        self.category_vars[category][asset] = asset_checkbox
        return asset_checkbox




    def check_asset_count(self):
        warnings_active = False  # Indique si un avertissement est actif dans au moins une catégorie

        for category in ["ratios", "ensembles"]:
            if category in self.category_vars:
                selected_assets = sum(1 for asset, checkbox in self.category_vars[category].items() if checkbox.isChecked())
                if selected_assets == 1:  # Avertissement pour un seul actif
                    self.warning_labels[category].setVisible(True)
                    warnings_active = True
                else:
                    self.warning_labels[category].setVisible(False)

        # Bloquer le bouton "Apply" si un avertissement est actif
        self.apply_button.setEnabled(not warnings_active)



    def enable_apply_button(self):
        self.apply_button.setEnabled(True)

    def save_selection(self):
        # Vérifier qu'aucun avertissement n'est actif avant d'enregistrer
        if not any(label.isVisible() for label in self.warning_labels.values()):
            for category, asset_vars in self.category_vars.items():
                self.current_config[category] = [asset for asset, var in asset_vars.items() if var.isChecked()]
            save_assets_to_backtest_config(self.current_config)
            self.apply_button.setEnabled(False)
            self.assets_saved.emit()


    def create_category_buttons(self, category: str) -> tuple:
        button_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        unselect_all_button = QPushButton("Unselect All")

        select_all_button.clicked.connect(lambda _, c=category: self.select_all(c))
        unselect_all_button.clicked.connect(lambda _, c=category: self.unselect_all(c))

        button_layout.addWidget(select_all_button)
        button_layout.addWidget(unselect_all_button)
        return button_layout, select_all_button, unselect_all_button

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
