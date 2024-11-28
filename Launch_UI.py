from PySide6.QtWidgets import (QWidget, 
                               QHBoxLayout, 
                               QVBoxLayout, 
                               QProgressBar, 
                               QMainWindow, 
                               QGridLayout, 
                               QSizePolicy, 
                               QSpacerItem,
                               QLabel)

from PySide6.QtGui import QPixmap, QIcon

from Files import (APP_ICON_PHOTO,
                    FONT_FAMILY, 
                    FONT_SIZE, 
                    FONT_TYPE)

from PySide6.QtWidgets import QApplication


def apply_global_styles(app:QApplication):
    app.setWindowIcon(QIcon(APP_ICON_PHOTO)) 
    app.setStyleSheet(f"""
        * {{
            font-family: '{FONT_FAMILY}';
            font-size: {FONT_SIZE};
            font: {FONT_TYPE};
        }}
    """)


def setup_launch_page(parent, title: str):
    # Fenêtre principale
    progress_window = QMainWindow(parent)
    progress_window.setWindowTitle(title)

    # Widget principal
    main_widget = QWidget(progress_window)
    main_layout = QVBoxLayout(main_widget)
    progress_window.setCentralWidget(main_widget)

    # 1er layout horizontal (stretch = 4)
    top_layout = QHBoxLayout()
    top_layout.setStretch(0, 4)

    # Grille 3x3 dans le premier layout
    grid_layout = QGridLayout()
    grid_layout.setContentsMargins(0, 0, 0, 0)  # Supprime les marges inutiles
    for row in range(3):
        for col in range(3):
            grid_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), row, col)

    # Ajouter le logo au centre (grille 3x3)
    logo_label = QLabel()
    pixmap = QPixmap(APP_ICON_PHOTO)
    logo_label.setPixmap(pixmap)
    logo_label.setScaledContents(True)  # Rend l'image responsive
    grid_layout.addWidget(logo_label, 1, 1)  # Cellule centrale
    # Ajouter la grille au layout principal
    top_layout.addLayout(grid_layout)
    main_layout.addLayout(top_layout, stretch=4)

    # 2ème layout horizontal (stretch = 1)
    bottom_layout = QHBoxLayout()

    # Séparer en 3 layouts verticaux égaux
    left_layout = QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    # Barre de chargement + pourcentage dans le layout central
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    center_layout.addWidget(progress_bar)

    # Ajouter les sous-layouts au layout horizontal
    bottom_layout.addLayout(left_layout, stretch=1)
    bottom_layout.addLayout(center_layout, stretch=4)
    bottom_layout.addLayout(right_layout, stretch=1)

    # Ajouter le 2ème layout au layout principal
    main_layout.addLayout(bottom_layout, stretch=1)
    progress_window.showMaximized()

    return progress_window, progress_bar