from PySide2.QtCore import QObject, QAbstractListModel
from Bio.SeqRecord import SeqRecord


class SequenceRecordItem(QObject):
    def __init__(self, parent,seq_rec):
        super(SequenceRecordItem, self).__init__(parent)
        self.seq_rec = seq_rec

    def select(self):
        self.m_selected = True

    def deselect(self):
        self.m_selected = False


    m_shift = 0
    m_selected = False
