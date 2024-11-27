from PySide6.QtWidgets import (QWidget, 
                               QHBoxLayout, 
                               QVBoxLayout, 
                               QProgressBar, 
                               QTextEdit, 
                               QDialog, 
                               QPushButton, 
                               QMainWindow, 
                               QApplication, 
                               QLineEdit, 
                               QGridLayout, 
                               QSizePolicy, 
                               QSpacerItem)
from PySide6.QtGui import QPalette, QBrush, QPixmap, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import tempfile
import os
import UI
import Dashboard

def generate_plot_widget(fig, show_legend:bool=True):
    if not show_legend:
        fig.update_layout(showlegend=False)

    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    html_content = html_content.replace("<body>", f"<body style='background-color: {UI.BACKGROUND_GRAPH_DARK};'>")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="outquant.html")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)
    plot_widget = QWebEngineView()
    plot_widget.load(QUrl.fromLocalFile(temp_file.name))
    return plot_widget


def apply_global_styles(app:QApplication):
    app.setWindowIcon(QIcon(UI.APP_ICON_PHOTO)) 
    app.setStyleSheet(f"""
        * {{
            font-family: '{UI.FONT_FAMILY}';
            font-size: {UI.FONT_SIZE};
            font: {UI.FONT_TYPE};
        }}
    """)

def cleanup_temp_files():
    # Supprimer tous les fichiers avec le suffixe 'outquant.html' dans le répertoire temporaire
    temp_dir = tempfile.gettempdir()
    for file_name in os.listdir(temp_dir):
        if file_name.endswith("outquant.html"):
            file_path = os.path.join(temp_dir, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier temporaire {file_path} : {e}")


def display_plot_dialog(parent, fig, window_title: str):
    plot_widget = generate_plot_widget(fig)
    plot_widget.showMaximized
    dialog = QDialog(parent)
    dialog.setWindowTitle(window_title)
    layout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.resize(1200, 800)
    dialog.exec()

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def setup_home_page(parent: QMainWindow, run_backtest_callback, open_config_callback, refresh_data_callback):

    parent.setWindowTitle("OutQuantLab")
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    set_background_image(main_widget, UI.HOME_PAGE_PHOTO,)

    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    main_layout.addWidget(backtest_button)

    config_button = QPushButton("Open Config")
    config_button.clicked.connect(open_config_callback)
    main_layout.addWidget(config_button)

    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    main_layout.addWidget(refresh_button)

    main_widget.setLayout(main_layout)
    parent.setCentralWidget(main_widget)

def setup_loading_page(parent):
    loading_widget = QWidget()
    loading_layout = QVBoxLayout(loading_widget)

    set_background_image(loading_widget, UI.LOADING_PAGE_PHOTO)
    loading_layout.addStretch()
    progress_bar = QProgressBar(loading_widget)
    progress_bar.setRange(0, 100)
    loading_layout.addWidget(progress_bar)

    log_output = QTextEdit(loading_widget)
    log_output.setReadOnly(True)
    log_output.setFixedHeight(100)
    loading_layout.addWidget(log_output)

    parent.setCentralWidget(loading_widget)

    return progress_bar, log_output

def setup_results_page(parent, plots, back_to_home_callback):
    results_widget = QWidget()
    results_layout = QHBoxLayout(results_widget)  # Layout principal horizontal
    # Définir l'image de fond
    set_background_image(results_widget, UI.DASHBOARD_PAGE_PHOTO)
    # Section gauche : Boutons de graphiques
    left_layout = QVBoxLayout()

    for title, plot_func in plots.items():
        button = QPushButton(title, results_widget)
        button.clicked.connect(plot_func)
        left_layout.addWidget(button)

    # Graphiques générés
    equity_plot = generate_plot_widget(Dashboard.plot_equity(parent.global_result), show_legend=False)
    sharpe_plot = generate_plot_widget(Dashboard.plot_rolling_sharpe_ratio(parent.global_result, length=1250), show_legend=False)
    drawdown_plot = generate_plot_widget(Dashboard.plot_rolling_drawdown(parent.global_result, length=1250), show_legend=False)
    vol_plot = generate_plot_widget(Dashboard.plot_rolling_volatility(parent.global_result), show_legend=False)

    # Layout pour la section supérieure droite
    right_top_layout = QHBoxLayout()

    # 1ère colonne : Horizontal Empty Space
    horizontal_empty_layout = QVBoxLayout()
    right_top_layout.addLayout(horizontal_empty_layout, stretch=6.5)  # Large espace vide

    # 2ème colonne : Input Fields Layout
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

    right_top_layout.addLayout(input_fields_layout, stretch=1)  # Section centrale (champs de saisie)

    # 3ème colonne : Back Home Layout
    back_home_layout = QVBoxLayout()
    back_to_home_button = QPushButton("Home Page")
    back_to_home_button.clicked.connect(back_to_home_callback)
    back_to_home_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # Dynamique mais fixe en hauteur
    back_home_layout.addWidget(back_to_home_button)
    # Ajouter un espace extensible sous le bouton
    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    back_home_layout.addItem(spacer)
    
    right_top_layout.addLayout(back_home_layout, stretch=0.5)

    # Grille pour les graphiques
    right_bottom_layout = QGridLayout()
    plots = [equity_plot, sharpe_plot, drawdown_plot, vol_plot]
    for i, plot in enumerate(plots):
        right_bottom_layout.addWidget(plot, i // 2, i % 2)  # Grille 2x2 pour les graphiques

    # Layout principal pour la section droite
    right_layout = QVBoxLayout()
    right_layout.addLayout(right_top_layout)  # Ajoute la division supérieure
    right_layout.addLayout(right_bottom_layout)  # Grille des graphiques

    # Ajouter les layouts gauche et droite au layout principal
    results_layout.addLayout(left_layout)  # Layout gauche
    results_layout.addLayout(right_layout)  # Layout droit

    parent.setCentralWidget(results_widget)

def setup_progress_bar(parent, title: str, max_value: int = 100):

    progress_window = QMainWindow(parent)
    progress_window.setWindowTitle(title)

    layout = QVBoxLayout()
    widget = QWidget(progress_window)
    progress_window.setCentralWidget(widget)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, max_value)
    layout.addWidget(progress_bar)

    widget.setLayout(layout)

    return progress_window, progress_bar

def update_progress_with_events(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()