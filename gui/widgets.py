from PyQt6.QtWidgets import QPlainTextEdit, QPushButton, QFileDialog, QWidget, QHBoxLayout, QLineEdit, QProgressBar, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
import math

class fileBrowser(QWidget):
    def __init__(self, parent=None):
        super(fileBrowser, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.setCheckable(True)
        self.textbox.setPlaceholderText("Enter filepath or click browse...")

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.textbox.setText(selected_files[0])


class directoryBrowser(QWidget):
    def __init__(self, parent=None):
        super(directoryBrowser, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit()
        self.button = QPushButton("Browse")
        self.button.setCheckable(True)
        self.textbox.setPlaceholderText("Enter filepath or click browse...")

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.textbox.setText(selected_files[0])


class linkInputBox(QWidget):
    def __init__(self, parent=None):
        super(linkInputBox, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.textbox = QPlainTextEdit()
        self.textbox.setPlaceholderText("Enter urls separated by line breaks...")

        layout.addWidget(self.textbox)

class progressBar(QWidget):
    def __init__(self, text, max_value, parent=None):
        super(progressBar, self).__init__(parent)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(text)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)


    def set_progress(self, value):
        self.progress_bar.setValue(value)


class SpinnerWidget(QWidget):
    def __init__(self, parent=None, size=30, num_dots=10, colour=QColor(0, 0, 0)):
        super(SpinnerWidget, self).__init__(parent)
        self.num_dots = num_dots
        self.colour = colour
        self.angle = 0

        self.setFixedSize(size, size)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

    def rotate(self):
        self.angle = (self.angle + 360 // self.num_dots) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height())
        centre = size / 2
        dot_radius = size / 10
        orbit_radius = size / 2 - dot_radius * 1.5

        for i in range(self.num_dots):
            angle = math.radians(self.angle + i * (360 / self.num_dots))

            x = centre + orbit_radius * math.cos(angle) - dot_radius
            y = centre + orbit_radius * math.sin(angle) - dot_radius

            opacity = (i + 1) / self.num_dots
            colour = QColor(self.colour)
            colour.setAlphaF(opacity)
            painter.setBrush(colour)
            painter.setPen(Qt.PenStyle.NoPen)

            painter.drawEllipse(int(x), int(y),
                                int(dot_radius * 2), int(dot_radius * 2))

    def start(self):
        self.timer.start(80)
        self.show()

    def stop(self):
        self.timer.stop()
        self.hide()
            