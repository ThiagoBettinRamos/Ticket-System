from app.views import ChamadosApp
import sys
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChamadosApp()
    window.run()
    sys.exit(app.exec())
