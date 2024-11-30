from typing import Dict, Any
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QSlider, QComboBox
from PySide6.QtCore import Qt, Signal
from .Config_Backend import save_param_config, param_range_values
from UI_Common import create_scroll_area, create_expandable_section, create_apply_button


class ParameterWidget(QWidget):
    parameters_saved = Signal()

    def __init__(self, current_config: Dict[str, Any]):
        super().__init__()
        self.current_config = current_config
        self.param_widgets = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create scrollable area using shared function
        scroll_area, scroll_widget, scroll_layout = create_scroll_area()

        for category, params in self.current_config.items():
            self.add_category_widget(category, params, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        layout.addWidget(scroll_area)

        # Create and add Apply button using shared function
        self.apply_button = create_apply_button(self.save_configuration)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, params: Dict[str, Any], layout: QVBoxLayout):
        # Use shared expandable section
        category_box, content_widget, content_layout = create_expandable_section(category)

        for param, values in params.items():
            self.add_param_widget(category, param, values, content_layout)

        layout.addWidget(category_box)

    def add_param_widget(self, category: str, param: str, values: list, layout: QVBoxLayout):
        param_box = QGroupBox(param)
        param_layout = QVBoxLayout()

        if not values:
            values = [1]

        # Informations dynamiques
        range_info_label, num_values_info_label, scroll_area = self.create_info_labels(values)
        param_layout.addWidget(range_info_label)
        param_layout.addWidget(num_values_info_label)
        param_layout.addWidget(scroll_area)

        # Sliders
        start_slider, end_slider = self.create_range_sliders(values)
        num_values_slider = self.create_num_values_slider(len(values))

        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(QLabel("Start:"))
        sliders_layout.addWidget(start_slider)
        sliders_layout.addWidget(QLabel("End:"))
        sliders_layout.addWidget(end_slider)
        param_layout.addLayout(sliders_layout)

        num_values_layout = QHBoxLayout()
        num_values_layout.addWidget(QLabel("Num Values:"))
        num_values_layout.addWidget(num_values_slider)
        param_layout.addLayout(num_values_layout)

        # Mode sélection
        mode_combobox = self.create_mode_combobox()
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(mode_combobox)
        param_layout.addLayout(mode_layout)

        # Connect sliders to update
        self.connect_sliders_to_update(
            category, param, start_slider, end_slider, num_values_slider, mode_combobox,
            range_info_label, num_values_info_label, scroll_area.widget(), param_box
        )

        param_box.setLayout(param_layout)
        layout.addWidget(param_box)

        self.param_widgets.setdefault(category, {})[param] = {
            "start_slider": start_slider,
            "end_slider": end_slider,
            "num_values_slider": num_values_slider,
            "mode_combobox": mode_combobox,
            "range_info_label": range_info_label,
            "num_values_info_label": num_values_info_label,
        }

    def create_info_labels(self, values: list):
        range_info_label = QLabel(f"Range: {min(values)} - {max(values)}")
        num_values_info_label = QLabel(f"Num Values: {len(values)}")

        # Generated values label
        generated_values_label = QLabel(f"Generated Values: {values}")
        generated_values_label.setWordWrap(False)

        # Scroll area for generated values using shared function
        scroll_area, _, _ = create_scroll_area()
        scroll_area.setWidget(generated_values_label)
        scroll_area.setFixedHeight(50)

        return range_info_label, num_values_info_label, scroll_area

    def create_range_sliders(self, values: list):
        start_slider = QSlider(Qt.Horizontal)
        end_slider = QSlider(Qt.Horizontal)

        start_slider.setMinimum(0)  # Index correspondant à 1
        start_slider.setMaximum(11)  # Index correspondant à 2048
        end_slider.setMinimum(0)  # Index correspondant à 1
        end_slider.setMaximum(12)  # Index correspondant à 4096

        start_slider.setValue(self.value_to_index(min(values)))
        end_slider.setValue(self.value_to_index(max(values)))

        return start_slider, end_slider

    def create_num_values_slider(self, num_values: int):
        num_values_slider = QSlider(Qt.Horizontal)
        num_values_slider.setMinimum(1)
        num_values_slider.setMaximum(10)
        num_values_slider.setValue(num_values)
        return num_values_slider

    def create_mode_combobox(self):
        mode_combobox = QComboBox()
        mode_combobox.addItems(["Linear", "Ratio"])
        return mode_combobox

    def value_to_index(self, value: int) -> int:
        return int(value).bit_length() - 1

    def index_to_value(self, index: int) -> int:
        return 2 ** index

    def connect_sliders_to_update(self, category, param, start_slider, end_slider, num_values_slider, mode_combobox,
                                  range_info_label, num_values_info_label, generated_values_label, param_box):
        def update_values():
            start = self.index_to_value(start_slider.value())
            end = self.index_to_value(end_slider.value())
            num_values = num_values_slider.value()
            mode = mode_combobox.currentText()

            # Enforce the 2x constraint: end >= 2 * start
            if start * 2 > end:
                if start_slider.hasFocus():
                    end_slider.setValue(self.value_to_index(start * 2))
                    end = self.index_to_value(end_slider.value())
                elif end_slider.hasFocus():
                    start_slider.setValue(self.value_to_index(end // 2))
                    start = self.index_to_value(start_slider.value())

            # Generate values and ensure uniqueness
            linear = (mode == "Linear")
            generated_values = param_range_values(start, end, num_values, linear=linear)

            # Limiter les doublons
            unique_values = list(sorted(set(generated_values)))
            while len(unique_values) < num_values:
                num_values -= 1
                unique_values = list(sorted(set(param_range_values(start, end, num_values, linear=linear))))

            # Update the num_values slider if reduced
            if num_values < num_values_slider.value():
                num_values_slider.setValue(num_values)

            # Update labels
            range_info_label.setText(f"Range: {start} - {end}")
            num_values_info_label.setText(f"Num Values: {num_values}")
            generated_values_label.setText(f"Generated Values: {unique_values}")

            # Mettre à jour self.current_config
            self.current_config[category][param] = unique_values

            # Activer le bouton Apply
            self.apply_button.setEnabled(True)

        start_slider.valueChanged.connect(update_values)
        end_slider.valueChanged.connect(update_values)
        num_values_slider.valueChanged.connect(update_values)
        mode_combobox.currentTextChanged.connect(update_values)

    def save_configuration(self):
        save_param_config(self.current_config)
        self.apply_button.setEnabled(False)
        self.parameters_saved.emit()

    def get_data(self) -> Dict[str, Any]:
        return self.current_config
