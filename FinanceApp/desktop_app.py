# desktop_app.py
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from app import app

# Function to run the Flask app
def run_flask_app():
    app.run(port=5000)

# PyQt5 Application
class FlaskApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flask Desktop App")
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl("http://localhost:5000"))

def main():
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    qt_app = QApplication(sys.argv)
    window = FlaskApp()
    window.show()
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()