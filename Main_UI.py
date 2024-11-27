from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QTextEdit, QDialog, QPushButton, QMainWindow, QApplication
from PySide6.QtGui import QPalette, QBrush, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import tempfile
import os

def apply_global_styles(app:QApplication):
    """
    Applique les styles globaux à l'application.
    """
    app.setStyleSheet("""
        * {
            font-family: 'QuickSand';
            font-size: 10px;
            font: bold;
        }
    """)

def cleanup_temp_files(temp_files: list):
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier temporaire {temp_file} : {e}")

def display_plot_dialog(parent, fig, window_title: str, default_width: int, default_height: int, background_color: str):
    """
    Crée et affiche un graphique Plotly dans un QDialog, tout en gérant les fichiers temporaires.
    """
    # Génère le HTML avec Plotly inclus
    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    html_content = html_content.replace("<body>", f"<body style='background-color: {background_color};'>")

    # Crée un fichier temporaire pour le HTML
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Crée un QWebEngineView et charge le fichier
    dialog = QDialog(parent)
    dialog.setWindowTitle(window_title)
    layout = QVBoxLayout(dialog)
    web_view = QWebEngineView(dialog)
    layout.addWidget(web_view)
    dialog.setLayout(layout)
    web_view.load(QUrl.fromLocalFile(temp_file.name))

    # Configure la taille et affiche le dialogue
    dialog.resize(default_width + 30, default_height + 40)
    dialog.exec()

    # Ajouter le fichier temporaire à la liste pour nettoyage ultérieur
    if hasattr(parent, 'temp_files'):
        parent.temp_files.append(temp_file.name)

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def update_progress(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):

    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)

def setup_home_page(parent, run_backtest_callback, open_config_callback, refresh_data_callback, background_image):
    """
    Configure la page d'accueil avec les boutons nécessaires.
    """
    main_widget = QWidget()
    main_layout = QVBoxLayout()

    set_background_image(main_widget, background_image)

    # Bouton Run Backtest
    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    main_layout.addWidget(backtest_button)

    # Bouton Open Config
    config_button = QPushButton("Open Config")
    config_button.clicked.connect(open_config_callback)
    main_layout.addWidget(config_button)

    # Bouton Refresh Data
    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    main_layout.addWidget(refresh_button)

    main_widget.setLayout(main_layout)
    parent.setCentralWidget(main_widget)

def create_loading_page(image_path: str):
    loading_widget = QWidget()
    loading_layout = QVBoxLayout(loading_widget)

    set_background_image(loading_widget, image_path)
    loading_layout.addStretch()
    progress_bar = QProgressBar(loading_widget)
    progress_bar.setRange(0, 100)
    loading_layout.addWidget(progress_bar)

    log_output = QTextEdit(loading_widget)
    log_output.setReadOnly(True)
    log_output.setFixedHeight(100)
    loading_layout.addWidget(log_output)

    return loading_widget, progress_bar, log_output

def setup_loading_page(parent, image_path):

    loading_widget, progress_bar, log_output = create_loading_page(image_path)
    parent.setCentralWidget(loading_widget)
    return progress_bar, log_output

def create_results_page(dashboard_plots, background_image, back_to_home_callback):

    results_widget = QWidget()
    results_layout = QVBoxLayout()

    # Définir l'image de fond
    set_background_image(results_widget, background_image)

    # Ajouter le bouton "Back to Home Page"
    back_to_home_button = QPushButton("Back to Home Page")
    back_to_home_button.clicked.connect(back_to_home_callback)
    results_layout.addWidget(back_to_home_button)

    # Ajouter les boutons pour chaque graphique
    for title, plot_func in dashboard_plots.items():
        button = QPushButton(title, results_widget)
        button.clicked.connect(plot_func)
        results_layout.addWidget(button)

    results_widget.setLayout(results_layout)
    return results_widget

def setup_results_page(parent, plots, background_image, back_to_home_callback):

    results_widget = create_results_page(
        dashboard_plots=plots,
        background_image=background_image,
        back_to_home_callback=back_to_home_callback,
    )
    parent.setCentralWidget(results_widget)

def setup_progress_bar(parent, title: str, max_value: int = 100):
    """
    Configure une barre de progression générique pour le chargement.
    """
    progress_window = QMainWindow(parent)
    progress_window.setWindowTitle(title)

    layout = QVBoxLayout()
    widget = QWidget(progress_window)
    progress_window.setCentralWidget(widget)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, max_value)
    layout.addWidget(progress_bar)

    widget.setLayout(layout)
    progress_window.resize(400, 200)

    return progress_window, progress_bar
