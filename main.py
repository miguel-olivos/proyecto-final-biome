import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from controlador_menu import ControladorMenu


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    try:
        controlador = ControladorMenu()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
        QMessageBox.critical(None, "Error", f"No se pudo iniciar:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()