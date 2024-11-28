from PySide6.QtWidgets import (QWidget, 
                               QHBoxLayout, 
                               QVBoxLayout, 
                               QProgressBar, 
                               QTextEdit,
                               QPushButton, 
                               QMainWindow, 
                               QApplication, 
                               QSizePolicy, 
                               QSpacerItem,
                               QLineEdit, 
                               QGridLayout,
                               QFrame
                               )
from PySide6.QtGui import QPalette, QBrush, QPixmap
from Files import ( 
                    BACKTEST_PAGE_PHOTO,
                    HOME_PAGE_PHOTO,
                    DASHBOARD_PAGE_PHOTO,
                    BACKGROUND_APP_DARK
                    )


def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def setup_home_page(parent: QMainWindow, run_backtest_callback, open_config_callback, refresh_data_callback):
    parent.setWindowTitle("OutQuantLab")

    # Widget principal et layout principal horizontal
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)

    # Moitié gauche
    left_layout = QVBoxLayout()

    # Layout pour les 80% de la hauteur gauche (vide)
    left_top_layout = QVBoxLayout()
    spacer_left_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    left_top_layout.addItem(spacer_left_top)

    # Layout pour les boutons en haut à gauche
    buttons_layout = QVBoxLayout()
    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    buttons_layout.addWidget(backtest_button)

    config_button = QPushButton("Open Config")
    config_button.clicked.connect(open_config_callback)
    buttons_layout.addWidget(config_button)

    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    buttons_layout.addWidget(refresh_button)

    # Ajouter les boutons en haut et l'espace vide en dessous
    left_layout.addLayout(buttons_layout)
    left_layout.addLayout(left_top_layout, stretch=4)

    # Moitié droite (vide, pleine hauteur)
    right_layout = QVBoxLayout()
    spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    right_layout.addItem(spacer_right)

    # Ajouter les layouts gauche et droite au layout principal
    main_layout.addLayout(left_layout, stretch=1)  # Moitié gauche
    main_layout.addLayout(right_layout, stretch=9)  # Moitié droite

    # Appliquer le layout principal au widget
    set_background_image(main_widget, HOME_PAGE_PHOTO)
    parent.setCentralWidget(main_widget)


def setup_backtest_page(parent):
    loading_widget = QWidget()
    main_layout = QVBoxLayout(loading_widget)
    set_background_image(loading_widget, BACKTEST_PAGE_PHOTO)
    # Premier layout horizontal (80% de la hauteur)
    top_layout = QHBoxLayout()
    main_layout.addLayout(top_layout, stretch=9)

    bottom_layout = QHBoxLayout()

    left_layout = QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    # Création du QFrame central
    center_frame = QFrame()
    center_frame.setFrameShape(QFrame.StyledPanel)
    center_frame.setFrameShadow(QFrame.Raised)
    center_frame.setStyleSheet(f"""
        QFrame {{
            border-radius: 15px;
            background-color: {BACKGROUND_APP_DARK};
        }}
    """)

    center_frame_layout = QVBoxLayout(center_frame)

    # Layout séparé pour la barre de progression
    progress_bar_layout = QVBoxLayout()
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar_layout.addWidget(progress_bar)

    # Layout séparé pour la zone de logs
    log_output_layout = QVBoxLayout()
    log_output = QTextEdit()
    log_output.setReadOnly(True)
    log_output_layout.addWidget(log_output)

    # Ajouter les deux sous-layouts au layout du QFrame central
    center_frame_layout.addLayout(progress_bar_layout)
    center_frame_layout.addLayout(log_output_layout)

    # Ajouter le QFrame central au layout central
    center_layout.addWidget(center_frame)

    # Ajouter les layouts verticaux au layout horizontal
    bottom_layout.addLayout(left_layout, stretch=1)
    bottom_layout.addLayout(center_layout, stretch=4)
    bottom_layout.addLayout(right_layout, stretch=1)
    # Ajouter le layout horizontal inférieur au layout principal
    main_layout.addLayout(bottom_layout, stretch=1)

    parent.setCentralWidget(loading_widget)
    return progress_bar, log_output


def setup_results_page(parent, plots, back_to_home_callback):
    results_widget = QWidget()
    results_layout = QHBoxLayout(results_widget)  # Layout principal horizontal
    set_background_image(results_widget, DASHBOARD_PAGE_PHOTO)

    # Section gauche : Boutons pour les graphiques
    left_layout = QVBoxLayout()
    for title, plot_func in plots.items():
        button = QPushButton(title, results_widget)
        button.clicked.connect(plot_func)
        left_layout.addWidget(button)

    # Layout pour la section supérieure droite (champs de saisie)
    right_top_layout = QHBoxLayout()
    input_fields_layout = QVBoxLayout()

    length_input = QLineEdit(results_widget)
    length_input.setPlaceholderText("Rolling length (e.g., 1250)")
    input_fields_layout.addWidget(length_input)

    max_clusters_input = QLineEdit(results_widget)
    max_clusters_input.setPlaceholderText("Max Clusters (e.g., 5)")
    input_fields_layout.addWidget(max_clusters_input)

    max_sub_clusters_input = QLineEdit(results_widget)
    max_sub_clusters_input.setPlaceholderText("Max Sub Clusters (e.g., 3)")
    input_fields_layout.addWidget(max_sub_clusters_input)

    max_sub_sub_clusters_input = QLineEdit(results_widget)
    max_sub_sub_clusters_input.setPlaceholderText("Max Sub Sub Clusters (e.g., 2)")
    input_fields_layout.addWidget(max_sub_sub_clusters_input)

    right_top_layout.addLayout(input_fields_layout, stretch=1)

    # Bouton pour revenir à la page d'accueil
    back_home_layout = QVBoxLayout()
    back_to_home_button = QPushButton("Home Page")
    back_to_home_button.clicked.connect(back_to_home_callback)
    back_home_layout.addWidget(back_to_home_button)

    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    back_home_layout.addItem(spacer)
    right_top_layout.addLayout(back_home_layout, stretch=0.5)

    # Layout pour les graphiques (grille vide)
    right_bottom_layout = QGridLayout()
    
    for i in range(2):  # 2 lignes
        for j in range(2):  # 2 colonnes
            placeholder = QWidget()
            right_bottom_layout.addWidget(placeholder, i, j)

    # Layout principal pour la section droite
    right_layout = QVBoxLayout()
    right_layout.addLayout(right_top_layout)
    right_layout.addLayout(right_bottom_layout)

    # Ajouter les layouts gauche et droit au layout principal
    results_layout.addLayout(left_layout)  # Layout gauche (boutons)
    results_layout.addLayout(right_layout)  # Layout droit (graphiques et champs)

    parent.setCentralWidget(results_widget)
    return right_bottom_layout  # Retourne la grille des graphiques


def update_progress_with_events(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()