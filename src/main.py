from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap
from widgets.mainwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap("resources/icon.png")))
    app.setApplicationName("docSaverPy")
    app.setApplicationDisplayName("docSaverPy")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("TrAyZeN")
    
    main_window = MainWindow()
    main_window.show()
    app.exec_()
