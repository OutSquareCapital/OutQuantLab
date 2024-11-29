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
                               QFrame,
                               QTableWidget,
                               QTableWidgetItem,
                               QLabel,
                               QSlider
                               )
from PySide6.QtGui import QPalette, QBrush, QPixmap
from Files import ( 
                    BACKTEST_PAGE_PHOTO,
                    HOME_PAGE_PHOTO,
                    DASHBOARD_PAGE_PHOTO,
                    BACKGROUND_APP_DARK
                    )
from PySide6.QtCore import Qt


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


def setup_results_page(parent, plots, back_to_home_callback, metrics):
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
    # Section droite : Sliders
    sliders_layout = QVBoxLayout()

    # Cluster sliders
    for i, label_text in enumerate(["Max Clusters", "Max Sub Clusters", "Max Sub-Sub Clusters"], 1):
        cluster_slider = QSlider(Qt.Horizontal)
        cluster_slider.setRange(0, 10)
        cluster_slider.setValue(5)  # Valeur par défaut
        cluster_label = QLabel(f"{label_text}: {cluster_slider.value()}")
        cluster_slider.valueChanged.connect(lambda value, lbl=cluster_label, lbl_txt=label_text: lbl.setText(f"{lbl_txt}: {value}"))
        sliders_layout.addWidget(cluster_label)
        sliders_layout.addWidget(cluster_slider)

    # Rolling length slider
    rolling_slider = QSlider(Qt.Horizontal)
    rolling_slider.setRange(6, 12)  # Log base 2 de 64 à 4096 (6 = log2(64), 12 = log2(4096))
    rolling_slider.setValue(10)  # log2(1024) comme valeur par défaut
    rolling_label = QLabel(f"Rolling Length: {2 ** rolling_slider.value()}")
    rolling_slider.valueChanged.connect(lambda value: rolling_label.setText(f"Rolling Length: {2 ** value}"))
    sliders_layout.addWidget(rolling_label)
    sliders_layout.addWidget(rolling_slider)

    # Leverage slider
    leverage_slider = QSlider(Qt.Horizontal)
    leverage_slider.setRange(1, 100)  # 0.1 à 10 avec des pas de 0.1 (100 * 0.1 = 10)
    leverage_slider.setValue(10)  # Par défaut, 1.0
    leverage_label = QLabel(f"Leverage: {leverage_slider.value() / 10:.1f}")
    leverage_slider.valueChanged.connect(lambda value: leverage_label.setText(f"Leverage: {value / 10:.1f}"))
    sliders_layout.addWidget(leverage_label)
    sliders_layout.addWidget(leverage_slider)


    # Bouton pour revenir à la page d'accueil
    back_home_layout = QVBoxLayout()
    back_to_home_button = QPushButton("Home Page")
    back_to_home_button.clicked.connect(back_to_home_callback)
    back_home_layout.addWidget(back_to_home_button)

    table_widget = QTableWidget(1, 5)
    results = [
        "Total Return %",
        "Average Rolling Drawdown",
        "Sharpe Ratio",
        "Volatility %",
        "Skewness"
    ]
    table_widget.setHorizontalHeaderLabels(results)

    for i, value in enumerate(metrics):
        item = QTableWidgetItem(f"{value}")
        item.setTextAlignment(Qt.AlignCenter)
        table_widget.setItem(0, i, item)

    right_top_layout.addWidget(table_widget, stretch=10)  # Le tableau à gauche
    right_top_layout.addLayout(sliders_layout, stretch=2)
    right_top_layout.addLayout(back_home_layout, stretch=1)

    # Création d'un QFrame pour right_bottom
    right_bottom_frame = QFrame()
    right_bottom_frame.setStyleSheet(f"""
        QFrame {{
            border-radius: 15px;
            background-color: {BACKGROUND_APP_DARK};
        }}
    """)

    # Layout interne pour le QFrame
    right_bottom_layout = QGridLayout(right_bottom_frame)
    right_bottom_layout.setHorizontalSpacing(0)
    right_bottom_layout.setVerticalSpacing(0)

    # Layout principal pour la section droite
    right_layout = QVBoxLayout()
    right_layout.addLayout(right_top_layout, stretch=1)
    right_layout.addWidget(right_bottom_frame, stretch=9)

    # Ajouter les layouts gauche et droit au layout principal
    results_layout.addLayout(left_layout, stretch=1)  # Layout gauche (boutons)
    results_layout.addLayout(right_layout, stretch=9)  # Layout droit (graphiques et champs)

    parent.setCentralWidget(results_widget)
    return right_bottom_layout  # Retourne la grille des graphiques


def update_progress_with_events(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()