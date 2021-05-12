import os
import pathlib
import traceback

from PySide2 import QtUiTools
from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide2.QtCore import QFile

from opengene.exceptions import UnrecognizedFileFormatError
from opengene.controllers import files
from opengene.views.sequence_widget import SequenceRecordsWindow


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = self.load_ui()
        self.main_widget.show()

        # Mdi Area setup

        # Signals-->Slots connections...
        self.main_widget.actionOpenFile.triggered.connect(self.load_file)


    def load_ui(self):
        loader = QtUiTools.QUiLoader()
        path = os.fspath(pathlib.Path(__file__).resolve().parent.parent / "ressources" / "mainwindow.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

    def load_file(self):
        file_names, _ = QFileDialog.getOpenFileNames(self.main_widget, caption=self.tr("Open File"), filter=self.tr("All Files (*);;"
                                                                                                "Fasta Files (*.fas);;"
                                                                                                "Edi Files (*.edi)")
                                                     )
        for file_name in file_names:
            try:
                self.add_seq_records(files.load_file(file_name))
            except UnrecognizedFileFormatError:  # TODO: ask user for file type if not recognized
                traceback.print_exc()
                QMessageBox.warning(self.main_widget, self.tr("Unrecognized file"),
                                    self.tr(f"OpenGene can't open the file \"{file_name}\"")
                                    )

    def add_seq_records(self, seq_records):
        if not hasattr(self, "seq_records_window"):
            self.setup_display_seq_records()
        self.seq_records_window.populate(seq_records)

    def setup_display_seq_records(self):
        self.seq_records_window = SequenceRecordsWindow(self.main_widget.mdiArea)
        self.main_widget.mdiArea.addSubWindow(self.seq_records_window)
        self.seq_records_window.destroyed.connect(self.destroy_seq_records_window)
        self.seq_records_window.show()

    def destroy_seq_records_window(self):
        delattr(self, "seq_records_window")

# HOW TODO : create new class for seq rec and for lines display
  #  def display_seq_records(self, seq_records):
