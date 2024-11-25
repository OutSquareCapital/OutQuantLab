from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QScrollArea, QLabel
)
from typing import Dict, List
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
        scroll_layout = QVBoxLayout()

        for category in self.current_config.keys():
            self.add_category_widget(category, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Labels d'avertissement spécifiques
        for category in ["ratios", "ensembles"]:
            warning_label = QLabel(f"At least two assets must be selected in '{category}'")
            warning_label.setStyleSheet("color: red;")
            warning_label.setVisible(False)
            self.warning_labels[category] = warning_label
            layout.addWidget(warning_label)

        # Bouton "Apply"
        self.apply_button = QPushButton("Apply selection")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.save_selection)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, layout: QVBoxLayout):
        category_box = QGroupBox(category)
        category_layout = QVBoxLayout()
        category_content_widget = QWidget()
        category_content_layout = QVBoxLayout()
        category_content_widget.setLayout(category_content_layout)

        # Ajout d'une animation pour replier/étendre
        category_content_widget.setMaximumHeight(0)
        animation = QPropertyAnimation(category_content_widget, b"maximumHeight")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutCubic)

        edit_button = QPushButton("Expand/Collapse")
        edit_button.setCheckable(True)
        edit_button.toggled.connect(
            lambda checked: self.toggle_animation(checked, category_content_widget, animation)
        )

        # Boutons "Select All" et "Unselect All"
        button_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        unselect_all_button = QPushButton("Unselect All")
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(unselect_all_button)

        select_all_button.clicked.connect(lambda _, c=category: self.select_all(c))
        unselect_all_button.clicked.connect(lambda _, c=category: self.unselect_all(c))

        # Checkboxes pour les actifs
        self.category_vars[category] = {}
        for asset in self.assets_names:
            asset_checkbox = self.create_asset_checkbox(category, asset)
            category_content_layout.addWidget(asset_checkbox)

        category_box.setLayout(category_layout)
        category_layout.addWidget(edit_button)
        category_layout.addLayout(button_layout)
        category_layout.addWidget(category_content_widget)
        layout.addWidget(category_box)

    def create_asset_checkbox(self, category: str, asset: str) -> QCheckBox:
        asset_checkbox = QCheckBox(asset)
        asset_checkbox.setChecked(asset in self.current_config.get(category, []))
        asset_checkbox.stateChanged.connect(self.check_asset_count)
        self.category_vars[category][asset] = asset_checkbox
        return asset_checkbox

    def toggle_animation(self, checked: bool, widget: QWidget, animation: QPropertyAnimation):
        if checked:
            animation.setStartValue(0)
            animation.setEndValue(widget.sizeHint().height())
        else:
            animation.setStartValue(widget.sizeHint().height())
            animation.setEndValue(0)
        animation.start()

    def check_asset_count(self):
        warnings_active = False
        for category in ["ratios", "ensembles"]:
            if category in self.category_vars:
                selected_assets = sum(
                    1 for asset, checkbox in self.category_vars[category].items() if checkbox.isChecked()
                )
                if selected_assets == 1:
                    self.warning_labels[category].setVisible(True)
                    warnings_active = True
                else:
                    self.warning_labels[category].setVisible(False)
        self.apply_button.setEnabled(not warnings_active)

    def save_selection(self):
        if not any(label.isVisible() for label in self.warning_labels.values()):
            for category, asset_vars in self.category_vars.items():
                self.current_config[category] = [
                    asset for asset, var in asset_vars.items() if var.isChecked()
                ]
            save_assets_to_backtest_config(self.current_config)
            self.apply_button.setEnabled(False)
            self.assets_saved.emit()

    def select_all(self, category: str):
        for var in self.category_vars[category].values():
            var.setChecked(True)
        self.check_asset_count()

    def unselect_all(self, category: str):
        for var in self.category_vars[category].values():
            var.setChecked(False)
        self.check_asset_count()

    def get_data(self) -> Dict[str, List[str]]:
        return self.current_config
