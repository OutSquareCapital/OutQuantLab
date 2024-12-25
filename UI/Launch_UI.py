from PySide6.QtWidgets import (
    QApplication,
    QWidget, 
    QHBoxLayout, 
    QVBoxLayout, 
    QProgressBar, 
    QMainWindow, 
    QGridLayout, 
    QSizePolicy, 
    QSpacerItem,
    QLabel)
from PySide6.QtGui import QPixmap, QIcon
from Files import (
    APP_ICON_PHOTO,
    FONT_FAMILY, 
    FONT_SIZE, 
    FONT_TYPE)
from typing import Any

def apply_global_styles(app:QApplication):
    app.setWindowIcon(QIcon(APP_ICON_PHOTO)) 
    app.setStyleSheet(f"""
        * {{
            font-family: '{FONT_FAMILY}';
            font-size: {FONT_SIZE}px;
            font: {FONT_TYPE};
        }}
    """)

def setup_launch_page(parent: Any) -> tuple[QMainWindow, QProgressBar]:
    progress_window = QMainWindow(parent)
    progress_window.setWindowTitle('OutQuantLab')

    main_widget = QWidget(progress_window)
    main_layout = QVBoxLayout(main_widget)
    progress_window.setCentralWidget(main_widget)

    top_layout = QHBoxLayout()
    top_layout.setStretch(0, 4)

    grid_layout = QGridLayout()
    grid_layout.setContentsMargins(0, 0, 0, 0)
    for row in range(3):
        for col in range(3):
            grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding), row, col)

    logo_label = QLabel()
    pixmap = QPixmap(APP_ICON_PHOTO)
    logo_label.setPixmap(pixmap)
    logo_label.setScaledContents(True) 
    grid_layout.addWidget(logo_label, 1, 1)
    top_layout.addLayout(grid_layout)
    main_layout.addLayout(top_layout, stretch=4)

    bottom_layout = QHBoxLayout()

    left_layout = QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    center_layout.addWidget(progress_bar)

    bottom_layout.addLayout(left_layout, stretch=1)
    bottom_layout.addLayout(center_layout, stretch=4)
    bottom_layout.addLayout(right_layout, stretch=1)

    main_layout.addLayout(bottom_layout, stretch=1)
    progress_window.showMaximized()

    return progress_window, progress_bar