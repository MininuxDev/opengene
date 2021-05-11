
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QFont, QFontMetrics
from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy, QToolButton, \
    QFrame, QSpinBox, QGridLayout, QSpacerItem, QScrollBar


class SequenceRecordsWindow(QWidget):
    def __init__(self, parent):
        super(SequenceRecordsWindow, self).__init__(parent)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)
        self.setLayout(self.grid_layout)

        self.seq_font = QFont()
        self.seq_font.setFamily("Noto Sans Mono")
        self.seq_font.setPointSize(12)
        self.seq_font.setFixedPitch(True)
        self.seq_font.setStyleHint(QFont.Monospace)

        self.seq_record_items = []

    def sizeHint(self):  # Workaroud QTBUG-70305
        return self.parent().parent().size()

    def populate(self, seq_records):
        self.clear()
        for seq_record in seq_records:
            row = self.grid_layout.rowCount()
            self.seq_record_items.append(SequenceRecordItem(self, seq_record, self.seq_font))
            for widget_index in range(0, len(self.seq_record_items[-1].widgets)):
                col = widget_index
                self.seq_record_items[-1].widgets[-1].installEventFilter(self)
                self.grid_layout.addWidget(self.seq_record_items[-1].widgets[widget_index], row, col)

            if len(seq_record) > self.longest_seq_len:
                self.longest_seq_len = len(seq_record)

        self.update_char_nb()
        self.seq_h_scroll_bar = QScrollBar(self, self.parent())
        self.seq_h_scroll_bar.setOrientation(Qt.Horizontal)
        self.seq_h_scroll_bar.setMinimum(0)
        self.seq_h_scroll_bar.setMaximum(self.longest_seq_len - self.char_nb)
        self.seq_h_scroll_bar.valueChanged.connect(self.move_seqs)

        self.grid_layout.addWidget(self.seq_h_scroll_bar, self.grid_layout.rowCount(), 5)
        self.grid_layout.addItem(QSpacerItem(1, 1))
        self.grid_layout.setRowStretch(self.grid_layout.rowCount(), 100)

        self.display_all_seq()

    def clear(self):
        # TODO
        pass

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Resize:
            self.update_char_nb()
            self.update_scrollbar()
            self.display_all_seq()
        return super(SequenceRecordsWindow, self).eventFilter(watched, event)


    def display_all_seq(self):
        for seq_record_item in self.seq_record_items:
            seq_record_item.seqLabel.display_seq(seq_record_item.seq_record.seq, self.display_begin, self.char_nb)

    def update_char_nb(self):
        font_metrics = QFontMetrics(self.seq_font)
        px_wide_char = font_metrics.width("A")
        label_width = self.seq_record_items[0].seqLabel.width()  # width of first seq label = all seq labels
        approx_char_nb = label_width // px_wide_char

        test_str = "A" * approx_char_nb

        while font_metrics.width(test_str) < label_width:  # fontMetrics not precise at all...
            test_str += "A"

        while font_metrics.width(test_str) >= label_width:  # fontMetrics not precise at all...
            test_str = test_str[:-1]

        self.char_nb = len(test_str)

    def update_scrollbar(self):
        self.seq_h_scroll_bar.setMaximum(self.longest_seq_len - self.char_nb + 12)

    def move_seqs(self, value):
        print(value)
        self.display_begin = value
        self.display_all_seq()

    char_nb = 0
    longest_seq_len = 0
    display_begin = 0


class SequenceRecordItem:
    def __init__(self, parent, seq_record, font):
        self.seq_record = seq_record
        self.parent = parent

        self.selectButton = QToolButton(parent)

        self.nameLabel = QLabel(parent)
        self.nameLabel.setFrameShape(QFrame.Box)
        self.nameLabel.setText(str(self.seq_record.name))

        self.shiftLeftButton = QToolButton(parent)
        self.shiftLeftButton.setArrowType(Qt.LeftArrow)
        self.shiftRightButton = QToolButton(parent)
        self.shiftRightButton.setArrowType(Qt.RightArrow)

        self.shiftSpinBox = QSpinBox(parent)
        self.shiftSpinBox.setFrame(True)
        self.shiftSpinBox.setButtonSymbols(QSpinBox.NoButtons)
        self.shiftSpinBox.setMinimum(-999999)
        self.shiftSpinBox.setMaximum(999999)
        self.shiftSpinBox.setValue(0)

        self.seqLabel = SequenceRecordLabel(parent, font)

        self.widgets = [self.selectButton, self.nameLabel, self.shiftLeftButton, self.shiftRightButton, self.shiftSpinBox, self.seqLabel]

        self.shiftRightButton.clicked.connect(self.shiftSpinBox.stepUp)
        self.shiftLeftButton.clicked.connect(self.shiftSpinBox.stepDown)

    selected = False
    shift = 0

    seq_select_beginning = 0
    seq_select_end = 0


class SequenceRecordLabel(QLabel):
    def __init__(self, parent, font):
        super(SequenceRecordLabel, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred))
        self.setFont(font)
        self.setStyleSheet("background: white")
        self.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)

    def minimumSizeHint(self):  # dirty workaround FIXME
        return QSize(40, 10)

    def sizeHint(self):  # dirty workaround FIXME
        return QSize(40, 10)

    def display_seq(self, seq, display_begin, char_nb):
        display_end = display_begin + char_nb
        self.setText(str(seq[display_begin:display_end]))