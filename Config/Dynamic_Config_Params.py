from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QWidget, QScrollArea, 
    QLabel, QLineEdit, QSlider, QComboBox, QSpinBox, QFormLayout
)
from .Dynamic_Config_Backend import load_param_config, save_param_config

class ParamManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parameter Manager")
        self.param_config = load_param_config()
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        for category, params in self.param_config.items():
            category_box = QGroupBox(category)
            category_layout = QVBoxLayout()
            for param_name, param_values in params.items():
                param_box = QGroupBox(param_name)
                param_layout = QFormLayout()

                # Input for manual values
                manual_input = QLineEdit()
                manual_input.setPlaceholderText("Enter values, separated by commas")
                manual_input.setText(",".join(map(str, param_values.get("manual", []))))
                manual_input.editingFinished.connect(
                    lambda p=param_name, c=category, inp=manual_input: self.update_manual_values(c, p, inp)
                )
                param_layout.addRow("Manual Values:", manual_input)

                # Range settings
                range_layout = QHBoxLayout()
                start_spin = QSpinBox()
                start_spin.setRange(1, 100000)
                start_spin.setValue(param_values.get("range", {}).get("start", 1))
                start_spin.valueChanged.connect(
                    lambda _, p=param_name, c=category, spin=start_spin: self.update_range(c, p, "start", spin)
                )

                end_spin = QSpinBox()
                end_spin.setRange(1, 100000)
                end_spin.setValue(param_values.get("range", {}).get("end", 100))
                end_spin.valueChanged.connect(
                    lambda _, p=param_name, c=category, spin=end_spin: self.update_range(c, p, "end", spin)
                )

                num_values_spin = QSpinBox()
                num_values_spin.setRange(1, 100)
                num_values_spin.setValue(param_values.get("range", {}).get("num_values", 10))
                num_values_spin.valueChanged.connect(
                    lambda _, p=param_name, c=category, spin=num_values_spin: self.update_range(c, p, "num_values", spin)
                )

                linear_dropdown = QComboBox()
                linear_dropdown.addItems(["Ratio", "Linear"])
                linear_dropdown.setCurrentText("Linear" if param_values.get("range", {}).get("linear", False) else "Ratio")
                linear_dropdown.currentTextChanged.connect(
                    lambda _, p=param_name, c=category, dropdown=linear_dropdown: self.update_range(
                        c, p, "linear", dropdown, convert_to_bool=True
                    )
                )

                range_layout.addWidget(QLabel("Start:"))
                range_layout.addWidget(start_spin)
                range_layout.addWidget(QLabel("End:"))
                range_layout.addWidget(end_spin)
                range_layout.addWidget(QLabel("Num:"))
                range_layout.addWidget(num_values_spin)
                range_layout.addWidget(QLabel("Mode:"))
                range_layout.addWidget(linear_dropdown)
                param_layout.addRow("Range Values:", range_layout)

                param_box.setLayout(param_layout)
                category_layout.addWidget(param_box)

            category_box.setLayout(category_layout)
            scroll_layout.addWidget(category_box)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        save_button = QPushButton("Save Configuration")
        save_button.clicked.connect(self.save_config)
        main_layout.addWidget(save_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def update_manual_values(self, category, param_name, input_field):
        values = input_field.text().split(",")
        try:
            values = [float(value.strip()) for value in values if value.strip()]
            self.param_config[category][param_name]["manual"] = values
        except ValueError:
            input_field.setText("")
            self.param_config[category][param_name]["manual"] = []

    def update_range(self, category, param_name, key, widget, convert_to_bool=False):
        value = widget.currentText() if convert_to_bool else widget.value()
        if convert_to_bool:
            value = value == "Linear"
        self.param_config[category][param_name].setdefault("range", {})[key] = value

    def save_config(self):
        save_param_config(self.param_config)
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = ParamManagerWindow()
    window.show()
    app.exec()
