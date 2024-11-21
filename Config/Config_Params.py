from typing import Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QPushButton, QLabel, QGroupBox, QHBoxLayout,
    QLineEdit, QSpinBox, QComboBox
)
from PySide6.QtCore import Signal
from .Config_Backend import save_param_config, param_range_values

class ParameterWidget(QWidget):
    parameters_saved = Signal()  # Signal pour indiquer que les paramètres ont été sauvegardés

    def __init__(self, current_config: Dict[str, Any]):
        super().__init__()
        self.current_config = current_config
        self.param_widgets = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        for category, params in self.current_config.items():
            self.add_category_widget(category, params, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Bouton "Apply"
        self.apply_button = QPushButton("Apply")
        self.apply_button.setEnabled(False)  # Grisé au départ
        self.apply_button.clicked.connect(self.save_configuration)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def create_manual_update_callback(self, category: str, param: str, manual_input: QLineEdit):
        def update_manual_values():
            try:
                values = list(map(int, manual_input.text().split(",")))
                self.current_config[category][param] = values
                self.apply_button.setEnabled(True)  # Activer le bouton Apply
            except ValueError:
                pass
        return update_manual_values

    def create_range_update_callback(self, category: str, param: str, start_spinbox, end_spinbox, num_values_spinbox, mode_combobox):
        def update_range_values():
            start = start_spinbox.value()
            end = end_spinbox.value()
            num_values = num_values_spinbox.value()
            mode = mode_combobox.currentText()

            if start >= end:
                return

            linear = (mode == "Linear")
            values = param_range_values(start, end, num_values, linear=linear)
            self.current_config[category][param] = values

            widget = self.param_widgets[category][param]
            widget["manual_input"].setText(", ".join(map(str, values)))
            self.apply_button.setEnabled(True)  # Activer le bouton Apply
        return update_range_values

    def save_configuration(self):
        save_param_config(self.current_config)
        self.apply_button.setEnabled(False)  # Désactiver le bouton après sauvegarde
        self.parameters_saved.emit()

    def add_category_widget(self, category: str, params: Dict[str, Any], layout: QVBoxLayout):
        category_box = QGroupBox(category)
        category_layout = QVBoxLayout()

        for param, values in params.items():
            self.add_param_widget(category, param, values, category_layout)

        category_box.setLayout(category_layout)
        layout.addWidget(category_box)

    def add_param_widget(self, category: str, param: str, values: list, layout: QVBoxLayout):
        param_box = QGroupBox(param)
        param_layout = QVBoxLayout()

        if not values:
            values = [0]

        # Ligne 1 : Manual Values
        manual_entry_layout = QHBoxLayout()
        manual_label = QLabel("Manual Values:")
        manual_input = QLineEdit(", ".join(map(str, values)))
        manual_input.textChanged.connect(self.create_manual_update_callback(category, param, manual_input))
        manual_entry_layout.addWidget(manual_label)
        manual_entry_layout.addWidget(manual_input)

        # Ligne 2 : Range
        range_layout = QHBoxLayout()
        range_label = QLabel("Range:")
        start_spinbox = QSpinBox()
        end_spinbox = QSpinBox()

        start_spinbox.setMaximum(10000)
        end_spinbox.setMaximum(10000)
        start_spinbox.setValue(min(values))
        end_spinbox.setValue(max(values))

        range_layout.addWidget(range_label)
        range_layout.addWidget(QLabel("Start:"))
        range_layout.addWidget(start_spinbox)
        range_layout.addWidget(QLabel("End:"))
        range_layout.addWidget(end_spinbox)

        # Ligne 3 : Num Values + Linear/Ratio
        num_values_layout = QHBoxLayout()
        num_values_label = QLabel("Num Values:")
        num_values_spinbox = QSpinBox()
        num_values_spinbox.setMinimum(1)
        num_values_spinbox.setMaximum(100)
        num_values_spinbox.setValue(len(values))

        mode_combobox = QComboBox()
        mode_combobox.addItems(["Linear", "Ratio"])

        num_values_layout.addWidget(num_values_label)
        num_values_layout.addWidget(num_values_spinbox)
        num_values_layout.addWidget(QLabel("Mode:"))
        num_values_layout.addWidget(mode_combobox)

        start_spinbox.valueChanged.connect(self.create_range_update_callback(category, param, start_spinbox, end_spinbox, num_values_spinbox, mode_combobox))
        end_spinbox.valueChanged.connect(self.create_range_update_callback(category, param, start_spinbox, end_spinbox, num_values_spinbox, mode_combobox))
        num_values_spinbox.valueChanged.connect(self.create_range_update_callback(category, param, start_spinbox, end_spinbox, num_values_spinbox, mode_combobox))
        mode_combobox.currentTextChanged.connect(self.create_range_update_callback(category, param, start_spinbox, end_spinbox, num_values_spinbox, mode_combobox))

        param_layout.addLayout(manual_entry_layout)
        param_layout.addLayout(range_layout)
        param_layout.addLayout(num_values_layout)
        param_box.setLayout(param_layout)
        layout.addWidget(param_box)

        self.param_widgets.setdefault(category, {})[param] = {
            "manual_input": manual_input,
            "start_spinbox": start_spinbox,
            "end_spinbox": end_spinbox,
            "num_values_spinbox": num_values_spinbox,
            "mode_combobox": mode_combobox
        }

    def get_data(self) -> Dict[str, Any]:
        return self.current_config
