# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QSettings, QCoreApplication
from opengene.views.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication([])
    QCoreApplication.setApplicationName("OpenGene")
    QCoreApplication.setOrganizationName("MininuxDev")
    main_window = MainWindow()
    sys.exit(app.exec_())
